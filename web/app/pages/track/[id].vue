<template>
    <div class="d-flex flex-column ga-6 pa-6 overflow-auto">
        <v-card v-if="!loading" :title="data.name" :subtitle="data.artist" color="deep-purple-accent-4">
            <v-card-text class="d-flex ga-2 flex-wrap">
                <v-btn @click="player.play(data.id)" prepend-icon="mdi-play" variant="outlined">Play</v-btn>
                <v-btn prepend-icon="mdi-playlist-plus" variant="outlined" @click="playlistDialog = data">Add to Playlist</v-btn>
                <v-btn prepend-icon="mdi-multicast" variant="outlined" @click="addSlice" :disabled="processing">Create Slice</v-btn>
            </v-card-text>
        </v-card>
        <v-card v-for="slice in slices" variant="outlined" :loading="processing" :disabled="processing">
            <v-card-text>
                <v-text-field variant="underlined" label="Titel" v-model="slice.name"></v-text-field>
                <v-text-field variant="underlined" label="Artist" v-model="slice.artist"></v-text-field>
                <v-range-slider color="deep-purple-accent-1" label="Time" :max="audio.duration" :min="0" :step="1" v-model="slice.range" class="align-center" hide-details>
                </v-range-slider>
                <div class="d-flex align-center ga-6 mt-6 flex-wrap">
                    <v-text-field
                        v-model="slice.range[0]"
                        density="compact"
                        variant="underlined"
                        label="Start Time (Seconds)"
                        hide-details
                        min-width="100"
                    ></v-text-field><v-btn @click="player.play(data.id, slice.range[0])" icon="mdi-play" density="comfortable" variant="outlined"></v-btn>
                    <v-text-field
                        v-model="slice.range[1]"
                        density="compact"
                        variant="underlined"
                        label="End Time (Seconds)"
                        hide-details
                        min-width="100"
                    ></v-text-field><v-btn @click="player.play(data.id, slice.range[1])" icon="mdi-play" density="comfortable" variant="outlined"></v-btn>
                </div>
            </v-card-text>
        </v-card>
        <v-card v-if="slices.length" color="deep-purple-accent-4" :disabled="processing" :loading="processing">
            <v-card-text>
                <v-autocomplete v-model="selectedPlaylists" chips closable-chips multiple clearable item-title="name" item-value="id" :items="playlists" v-model:search="playlistSearch" :loading="playlistLoading" prepend-icon="mdi-playlist-music" label="Playlist" variant="outlined" placeholder="Type to search ..."></v-autocomplete>
                <div class="d-flex align-center ga-4 flex-wrap">
                    <v-btn :loading="processing" @click="saveData" prepend-icon="mdi-content-save" variant="outlined">Save Slices</v-btn>
                    <v-checkbox-btn hide-details inline label="Delete Original Track"></v-checkbox-btn>
                </div>
            </v-card-text>
        </v-card>
        <v-dialog
            v-model="playlistDialog"
            max-width="500"
            :fullscreen="mobile"
        >
            <add-song-to-playlist @close="playlistDialog=false" :track="playlistDialog"></add-song-to-playlist>
        </v-dialog>
        <v-dialog
            v-model="processingResults"
            max-width="500"
            :fullscreen="mobile"
        >
            <v-card
                prepend-icon="mdi-multicast"
                title="Slices Created"
                subtitle="The following slices have been created."
            >
            <v-list density="compact">
                <v-list-item v-for="item in processingResults">
                    <v-list-item-title>{{ item.name }}</v-list-item-title>
                    <v-list-item-subtitle>{{ item.artist }}</v-list-item-subtitle>
                </v-list-item>
            </v-list>
                <template v-slot:actions>
                    <v-btn
                        class="ms-auto"
                        text="Ok"
                        @click="processingResults = false"
                    ></v-btn>
                </template>
            </v-card>
        </v-dialog>
    </div>
</template>
<script setup>
import apiFetch from '~/fetch';

const runtimeConfig = useRuntimeConfig()
let backendUrl = runtimeConfig.public.backendUrl

const route = useRoute()
const player = usePlayerStore()
const loading = ref(true)

 /* Playlist add */
const { mobile } = useDisplay()
const playlistDialog = ref(false)

/* Slices */
const slices = ref([])
const data = await apiFetch('tracks/' + route.params.id)
const audio = new Audio(`${backendUrl}/library/stream/${data.id}`)
const processing = ref(false)
const processingResults = ref(false)
audio.autoplay = false
loading.value = false

const addSlice = async () => {
    slices.value.push({
        name: data.name,
        artist: data.artist,
        range: [1, 1]
    })
}

const saveData = async () => {
    processing.value = true
    processingResults.value = await apiFetch(`tracks/${data.id}/create_slices/`, {
        method: 'POST',
        body: {"slices": slices.value, "playlists": selectedPlaylists.value }
    })
    processing.value = false
    slices.value = []
}

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