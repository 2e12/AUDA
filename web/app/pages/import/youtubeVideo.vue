<template>
    <v-container class="fill-height">
        <v-card class="align-center v-col-12" title="Import from Youtube" flat>
            <v-card-text v-if="errorMessage">
                <v-alert
                    border="top"
                    type="warning"
                    variant="outlined"
                    prominent
                    >
                    {{ errorMessage }}           
                </v-alert>    
            </v-card-text>
            <v-card-text>
                <v-text-field :disabled="loading" v-model="youtubeLink" prepend-icon="mdi-youtube" label="YouTube Video Link" variant="outlined"></v-text-field>
                <v-autocomplete :disabled="loading" v-model="selectedPlaylists" chips closable-chips multiple clearable item-title="name" item-value="id" :items="playlists" v-model:search="playlistSearch" :loading="playlistLoading" prepend-icon="mdi-playlist-music" label="Playlist" variant="outlined"></v-autocomplete>
                <v-text-field :disabled="loading" variant="outlined" label="Titel" v-model="name"></v-text-field>
                <v-text-field :disabled="loading" variant="outlined" label="Artist" v-model="artist"></v-text-field>
            </v-card-text>
            <template v-slot:actions>
                <v-btn :disabled="loading" :loading="loading" block @click="upload(file, name)" variant="flat" color="deep-purple-accent-4" type="submit">Upload</v-btn>
            </template>
        </v-card>
    </v-container>
</template>

<script setup>
import apiFetch from '~/fetch';

const loading = ref(false)
const errorMessage = ref(false)

const upload = async (uploadFile, uploadName) => {
    errorMessage.value = false
    loading.value = true
    let data = await apiFetch('tracks/load_youtube_video/', {
        method: 'POST',
        body: {
            "youtube_link": youtubeLink.value,
            "playlists": selectedPlaylists.value,
            "name": name.value,
            "artist": artist.value
        },
    }).finally(() => {
        loading.value = false
    }).catch((error) => {
        debugger
        errorMessage.value = `Error fetching data: ${error.message}`
    })
    if(data) {
        youtubeLink.value = ""
        name.value = ""
    }
}

/* YouTube Video */
const youtubeLink = ref("")
const name = ref("")
const artist = ref("")

/* Playlist Select */
const playlistSearch = ref("")
const playlistLoading = ref(false)
const playlists = ref([])
const selectedPlaylists = ref([])

watch(playlistSearch, async(newValue, oldValue) => {
    playlistLoading.value = true
    let uri = 'playlists/?limit=8&search=' + newValue
    const data = await apiFetch(uri)
    playlists.value = data.results
    playlistLoading.value = false
})
</script>