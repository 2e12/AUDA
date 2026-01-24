<template>
    <v-list>
        <div class="px-4 pt-2 d-flex align-center justify-space-between">
            <h1>Queue</h1>
        </div>
        <draggable 
            v-model="player.queue" 
            item-key="data.id">
            <template #item="{element}">
                <v-list-item class="cursor-grab" prepend-icon="mdi-drag">{{ element.data.name }}</v-list-item>
            </template>
        </draggable>
    </v-list>
</template>
<script setup>
    import draggable from 'vuedraggable'
    const player = usePlayerStore()
    const drag = ref(false)
</script>