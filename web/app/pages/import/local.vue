<template>
    <v-container class="fill-height">
        <v-card class="align-center v-col-12" title="Upload" flat v-if="!loading">
            <v-card-text>
                Upload a new Track
            </v-card-text>
            <v-card-text>
                <v-file-input v-model="file" prepend-icon="mdi-file-music" label="Select File" accept="audio/*" variant="outlined"></v-file-input>
                <v-autocomplete v-model="selectedPlaylists" chips closable-chips multiple clearable item-title="name" item-value="id" :items="playlists" v-model:search="playlistSearch" :loading="playlistLoading" prepend-icon="mdi-playlist-music" label="Playlist" variant="outlined"></v-autocomplete>
            </v-card-text>
            <template v-slot:actions>
                <v-btn block @click="upload(file, name)" variant="flat" color="deep-purple-accent-4" type="submit">Upload</v-btn>
            </template>
        </v-card>
        <div class="align-center v-col-12 d-flex justify-center flex-column" v-if="loading">
            <v-progress-circular indeterminate class="mb-8" size="large"></v-progress-circular> Processing data
        </div>
    </v-container>
</template>

<script setup>
import apiFetch from '~/fetch';

const file = ref()
const name = ref("")
const loading = ref(false)
const upload = async (uploadFile, uploadName) => {
    loading.value = true
    let formData = new FormData();
    formData.append('source', "local");
    formData.append('file', uploadFile);
    formData.append('name', uploadName);
    formData.append('playlists', selectedPlaylists.value)
    let data = await apiFetch('tracks/upload_file/', {
        method: 'POST',
        body: formData,
    })
    file.value = null
    name.value = ""
    loading.value = false
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