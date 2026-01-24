<template>
    <div>
        <div class="px-4 pt-2 d-flex align-center justify-space-between ">
            <h1 v-if="playlist" class="mr-4">{{ playlist.name }}</h1>
            <div>
                <v-btn @click="addToQueue" color="deep-purple-accent-4" icon="mdi-play"></v-btn>
            </div>
        </div>
        <track-list @load-items="loadItems" :uri-params="{'playlists': route.params.id}"></track-list>
    </div>
</template>
<script setup>
    import apiFetch from '~/fetch';
    const route = useRoute()
    const playlist = await apiFetch('playlists/' + route.params.id)
    const player = usePlayerStore()
    let items = []

    const addToQueue = () => {
        const ids = []
        items.forEach(item => ids.push(item.id))
        player.addListToQueue(ids)
    }

    const loadItems = (loadedItems) => {
        items = loadedItems
    }
</script>