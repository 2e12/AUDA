<template>
    <v-container class="fill-height">
        <v-card class="align-center v-col-12" title="Import YouTube Playlist" flat v-if="!videos">
            <v-card-text v-if="errorMessage">
                <v-alert
                    type="warning"
                    variant="outlined"
                    prominent
                    >
                    {{ errorMessage }}           
                </v-alert>    
            </v-card-text>
            <v-card-text>
                <v-text-field v-model="youtubePlaylistLink" prepend-icon="mdi-youtube" label="YouTube Playlist Link" variant="outlined"></v-text-field>
                <v-text-field variant="outlined" label="Artist" v-model="artist"></v-text-field>
            </v-card-text>
            <template v-slot:actions>
                <v-btn block @click="loadVideos" :disabled="loading" :loading="loading" variant="flat" color="deep-purple-accent-4" type="submit">Upload</v-btn>
            </template>
        </v-card>
        <div class="align-center v-col-12" v-if="!loading && videos">
            <h1 class="mb-4">Playlist Details</h1>
            <v-text-field label="Playlist Name" v-model="playlist_name" variant="outlined"></v-text-field>
            <h1 class="mb-4">Video Details</h1>
            <template v-for="video in videos">
                <v-card variant="outlined" class="my-4" :loading="video.loading" v-if="!video.state">
                    <v-card-text>
                        <v-text-field :disabled="!editable" variant="underlined" label="Titel" v-model="video.name"></v-text-field>
                        <v-text-field :disabled="!editable" variant="underlined" label="Artist" v-model="video.artist"></v-text-field>
                        <a :href="video.url">{{ video.url }}</a>
                    </v-card-text>
                </v-card>
                <v-card variant="tonal" color="green" class="my-4" append-icon="mdi-check-bold" :title="video.name" :subtitle="video.artist" v-else-if="video.state === 'success'"></v-card>
                <v-card variant="tonal" color="red" class="my-4" append-icon="mdi-alert-circle-outline" :title="video.name" :subtitle="video.artist" v-else></v-card>
            </template>
            <v-btn class="mb-16" :disabled="!editable" color="deep-purple-accent-4" variant="flat" @click="processData">Process Playlist</v-btn>
        </div>
    </v-container>
</template>

<script setup>
import apiFetch from '~/fetch';

const router = useRouter()

const errorMessage = ref(false)

/* YouTube Playlist */
const youtubePlaylistLink = ref("")
const youtubeVideos = ref("")
const artist = ref("")

/* Video Preview */
const videos = ref(false)
const playlist_name = ref("")
const editable = ref(true)

/* Local Source */
const loading = ref(false)
const loadVideos = async () => {
    loading.value = true
    let data = await apiFetch('tracks/fetch_youtube_playlist/', {
        method: 'post',
        body: {
            'youtube_playlist_link': youtubePlaylistLink.value
        },
    }).catch((error) => {
        errorMessage.value = `Error fetching data: ${error.message}`
    })
    videos.value = data.videos
    if (artist.value) {
        videos.value.forEach((video) => video.artist = artist.value)
    }
    playlist_name.value = data.playlist_name
    loading.value = false
    youtubePlaylistLink.value = ""
}

const processData = async () => {
    editable.value = false
    const results = await apiFetch("playlists/", {
        method: "post",
        body: {
            name: playlist_name.value
        }
    })
    const playlist_id = results.id
    for (let video of videos.value ) {
        video.loading = true
        let data = await apiFetch('tracks/load_youtube_video/', {
            method: 'POST',
            body: {
                "youtube_link": video.url,
                "name": video.name,
                "artist": video.artist,
                "playlists": [playlist_id]
            },
            retry: 3,
            retryDelay: 5000,
            onResponseError: ({ request, options, error }) => {
                video.state = "error"
            },
            onResponse: ({ request, options, response }) => {
                video.id = response.body.id
                video.state = "success"
            }
        }).catch((error) => video.state = "error");
        video.loading = false
    }
    router.push(`/playlist/${playlist_id}`)
}
</script>