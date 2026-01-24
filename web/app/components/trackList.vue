<template>
    <div>
        <v-text-field v-model="search" prepend-inner-icon="mdi-magnify" class="ma-0 border-b-thin" variant="flat" hide-details></v-text-field>
        <v-data-table-server hide-default-header :items-per-page="25" :items-per-page-options="[25, 50, 100]" disable-sort class="fill-height" :loading="loading" :items-length="totalItems" :headers="headers" :search="search" :items="items" @update:options="tableUpdate">
            <template v-slot:loading>
                <v-skeleton-loader type="table-row@3"></v-skeleton-loader>
            </template>
            <template v-slot:item.actions="{ item }">
                <v-btn @click="player.play(item.id)" size="small" icon="mdi-play" variant="tonal"></v-btn>
                <v-menu>
                    <template v-slot:activator="{ props }">
                        <v-btn v-bind="props" size="small" icon="mdi-dots-vertical" variant="plain"></v-btn>
                    </template>
                    <v-list>
                        <v-list-item prepend-icon="mdi-pencil" @click="showEditDialog = item">
                            Edit
                        </v-list-item>
                        <v-list-item prepend-icon="mdi-multicast" :to="`/track/${item.id}/`">
                            Slice
                        </v-list-item>
                        <v-divider></v-divider>
                        <v-list-item prepend-icon="mdi-playlist-plus" @click="playlistDialog = item">
                            Add to Playlist
                        </v-list-item>
                        <v-list-item prepend-icon="mdi-tray-plus" @click="player.addToQueue(item.id)">
                            Add to Queue
                        </v-list-item>
                        <v-divider></v-divider>
                        <v-list-item prepend-icon="mdi-trash-can" @click="deleteTrack(item.id)">
                            Delete
                        </v-list-item>
                    </v-list>
                </v-menu>
            </template>
            <template v-slot:item.name="{ value }">
                <span class="font-weight-semibold">{{ value }}</span>
            </template>
        </v-data-table-server>
        <v-dialog
            v-model="playlistDialog"
            max-width="500"
            :fullscreen="mobile"
        >
            <add-song-to-playlist @close="playlistDialog=false" :track="playlistDialog"></add-song-to-playlist>
        </v-dialog>
        <v-dialog v-model="showEditDialog" max-width="500">
            <v-card
                title="Edit Track"
                :loading="editDialogLoading"
                :disabled="editDialogLoading"
            >
                <v-card-text>
                    <v-text-field v-model="showEditDialog.name" label="Title" variant="outlined"></v-text-field>
                    <v-text-field v-model="showEditDialog.artist" label="Artist" variant="outlined"></v-text-field>
                </v-card-text>
                <template v-slot:actions>
                    <v-btn
                        @click="showEditDialog = false"
                        flat
                        text="Cancel"
                    ></v-btn>
                    <v-btn
                        color="deep-purple-accent-4"
                        text="Save"
                        @click="saveTrack()"
                    ></v-btn>
                </template>
            </v-card>
        </v-dialog>
    </div>
</template>

<script setup>
    import apiFetch from '~/fetch';

    /* Edit Track */
    const showEditDialog = ref(false)
    const editDialogLoading = ref(false)
    const saveTrack = async () => {
        editDialogLoading.value = true
        const results = await apiFetch(`tracks/${showEditDialog.value.id}/`, {
            method: "patch",
            body: {
                name: showEditDialog.value.name,
                artist: showEditDialog.value.artist
            }
        })
        showEditDialog.value = false
        editDialogLoading.value = false
        await fetchData()
    }

    /* Misc */
    const playlistDialog = ref(false)
    const loading = ref(false)
    const player = usePlayerStore()
    const { mobile } = useDisplay()

    /* Items Callback */
    const emit = defineEmits(['loadItems'])

    /* Endpoint options */
    const props = defineProps({ uriParams: Object })
    const uriParams = new URLSearchParams()
    if (props.uriParams) {
        for (const [key, value] of Object.entries(props.uriParams)) {
           uriParams.set(key, value)
        }
    }

    /* Sorting */
    const items = ref([])
    const search = ref("")
    const totalItems = ref(0)
    
    const headers =[
        { title: 'Title', value: 'name' },
        { title: 'Artist', value: 'artist' },
        { title: 'Actions', value: 'actions', align: 'end' },
    ]

    const tableUpdate = async ({ page, itemsPerPage, sortBy, search }) => {
        uriParams.delete("search")
        uriParams.set("limit", itemsPerPage)
        uriParams.set("offset", (page-1) * itemsPerPage)
        if(search != "") {
            uriParams.set("search", search)
        }
        fetchData()
    }

    const fetchData = async () => {
        loading.value = true
        const data = await apiFetch(`tracks/?${uriParams}`)
        items.value = data.results
        emit("loadItems", data.results)
        totalItems.value = data.count
        loading.value = false
    }


    const deleteTrack = async(trackId) => {
        loading.value = true
        const results = await apiFetch(`tracks/${trackId}/`, { method: "delete" })
        await fetchData()
    }
</script>