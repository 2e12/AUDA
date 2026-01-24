<template>
    <v-card
        prepend-icon="mdi-playlist-music"
        title="Add to Playlist"
        :loading="loading"
        :disabled="loading"
    >
    <v-list density="compact">
        <v-list-item>
            <v-text-field v-model="search" hide-details label="Search" variant="outlined" density="compact" @update:model-value="fetchPlaylists"></v-text-field>
        </v-list-item>
        <v-divider v-if="selectedPlaylists.length"></v-divider>
        <v-list-item v-for="playlist in selectedPlaylists" :title="playlist.name">
            <template v-slot:prepend>
                <v-list-item-action start>
                    <v-checkbox-btn :value="playlist.id" v-model="selected"></v-checkbox-btn>
                </v-list-item-action>
            </template>
        </v-list-item>
        <v-divider></v-divider>
        <v-list-item v-for="playlist in items" :title="playlist.name">
            <template v-slot:prepend>
                <v-list-item-action start>
                    <v-checkbox-btn :value="playlist.id" v-model="selected"></v-checkbox-btn>
                </v-list-item-action>
            </template>
        </v-list-item>
        <v-divider></v-divider>
    </v-list>
        <template v-slot:actions>
            <v-btn
                class="ms-auto"
                text="Save"
                @click="save"
            ></v-btn>
        </template>
    </v-card>
</template>
<script setup>
    import apiFetch from '~/fetch';
    const emit = defineEmits(['close'])
    const loading = ref(true)
    const props = defineProps(['track'])
    const selected = ref([])
    const uri = `tracks/${props.track.id}/show_playlists/`
    const selectedPlaylists = await apiFetch(uri)
    const originallySelectedIds = []
    selectedPlaylists.forEach(playlist => {
        selected.value.push(playlist.id)
        originallySelectedIds.push(playlist.id)
    })
    loading.value = false
    
    const search = ref("")
    const items = ref([])
    const fetchPlaylists =  async () => {
        let uri = 'playlists/?limit=6'
        if(search.value != "") {
            uri += "&search=" + search.value
        }
        const data = await apiFetch(uri)
        items.value = data.results.filter(playlist => !(originallySelectedIds.includes(playlist.id)))
    }
    await fetchPlaylists()

    const save = async () => {
        if(!selected.value.length) {
            emit('close')
            return
        }
        loading.value = true
        const results = await apiFetch(`tracks/${props.track.id}/`, {
            method: "patch",
            body: {
                playlists: selected.value
            }
        })
        emit('close')
        loading.value = false
    }
</script>