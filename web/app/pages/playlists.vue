<template>
    <div>
        <div class="px-4 pt-2 d-flex align-center justify-space-between ">
            <h1>Playlists</h1>
            <div>
                <v-btn @click="showCreateDialog = true" color="deep-purple-accent-4" icon="mdi-plus"></v-btn>
            </div>
        </div>
        <v-text-field v-model="search" prepend-inner-icon="mdi-magnify" class="ma-0 border-b-thin" variant="flat" hide-details></v-text-field>
        <v-data-table-server hide-default-header :items-per-page="25" :items-per-page-options="[25, 50, 100]" disable-sort class="fill-height" :loading="loading" :items-length="totalItems" :headers="headers" :search="search" :items="items" @update:options="tableUpdate">
            <template v-slot:loading>
                <v-skeleton-loader type="table-row@10"></v-skeleton-loader>
            </template>
            <template v-slot:item="{ item }">
                <tr class="cursor-pointer">
                    <td @click="openPlaylist('/playlist/' + item.id)" v-ripple>
                        {{ item.name }}
                    </td>
                    <td class="v-data-table-column--align-end">
                        <v-btn @click="showEditDialog = item" size="small" icon="mdi-pencil" variant="plain"></v-btn>
                        <v-menu>
                            <template v-slot:activator="{ props }">
                                <v-btn v-bind="props" size="small" icon="mdi-dots-vertical" variant="plain"></v-btn>
                            </template>
                            <v-list>
                                <v-list-item @click="showDeleteDialog = item" prepend-icon="mdi-trash-can">
                                    Delete
                                </v-list-item>
                            </v-list>
                        </v-menu>
                    </td>
                </tr>
            </template>
        </v-data-table-server>
        <v-dialog v-model="showCreateDialog" max-width="500" :fullscreen="mobile">
            <v-card
                title="Create new Playlist"
                :loading="createDialogLoading"
                :disabled="createDialogLoading"
            >
                <v-card-text>
                    <v-text-field autofocus v-model="playlistName" label="Name" variant="outlined"></v-text-field>
                </v-card-text>
                <template v-slot:actions>
                    <v-btn
                        @click="showCreateDialog = false"
                        flat
                        text="Cancel"
                    ></v-btn>
                    <v-btn
                        color="deep-purple-accent-4"
                        text="Save"
                        :disabled="!playlistName"
                        @click="createPlaylist"
                    ></v-btn>
                </template>
            </v-card>
        </v-dialog>
        <v-dialog v-model="showEditDialog" max-width="500" :fullscreen="mobile">
            <v-card
                title="Edit Playlist"
                :loading="editDialogLoading"
                :disabled="editDialogLoading"
            >
                <v-card-text>
                    <v-text-field autofocus v-model="showEditDialog.name" label="Title" variant="outlined"></v-text-field>
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
                        @click="savePlaylist()"
                    ></v-btn>
                </template>
            </v-card>
        </v-dialog>
        <v-dialog v-model="showDeleteDialog" max-width="500" :fullscreen="mobile">
            <v-card
                title="Delete Playlist"
                :loading="deleteDialogLoading"
                :disabled="deleteDialogLoading"
            >
                <v-card-text>
                    <v-checkbox v-model="deleteRelated" label="Delete releated Tracks"></v-checkbox>
                </v-card-text>
                <template v-slot:actions>
                    <v-btn
                        @click="showDeleteDialog = false"
                        flat
                        text="Cancel"
                    ></v-btn>
                    <v-btn
                        color="red"
                        variant="tonal"
                        text="Delete"
                        @click="deletePlaylist"
                    ></v-btn>
                </template>
            </v-card>
        </v-dialog>
    </div>
</template>
<script setup>
    import apiFetch from '~/fetch';

    /* Delete Playlist */
    const showDeleteDialog = ref(false)
    const deleteDialogLoading = ref(false)
    const deleteRelated = ref(false)
    const deletePlaylist = async () => {
        deleteDialogLoading.value = true
        if(deleteRelated.value) {
            const songs = []
            const uriParams = new URLSearchParams()
            uriParams.set("playlists", showDeleteDialog.value.id)
            uriParams.set("limit", 50)
            while (true) {
                const uri = `/tracks/?${uriParams}`
                const data = await apiFetch(uri)
                songs.push(...data.results)
                if(data.next) {
                    const next = new URL(data.next)
                    uriParams.set("limit", next.searchParams.get("limit"))
                    uriParams.set("offset", next.searchParams.get("offset"))
                } else {
                    break
                }
            }
            for(let song of songs) {
                await apiFetch(`tracks/${song.id}/`, {
                    method: "delete"
                })
            }
        }
        await apiFetch(`playlists/${showDeleteDialog.value.id}/`, {
            method: "delete"
        })
        showDeleteDialog.value = false
        deleteDialogLoading.value = false
        deleteRelated.value = false
        await fetchData()
    }

    /* Edit Playlist */
    const showEditDialog = ref(false)
    const editDialogLoading = ref(false)
    const savePlaylist = async () => {
        editDialogLoading.value = true
        await apiFetch(`playlists/${showEditDialog.value.id}/`, {
            method: "patch",
            body: {
                name: showEditDialog.value.name,
            }
        })
        showEditDialog.value = false
        editDialogLoading.value = false
        await fetchData()
    }

    /* Misc */
    const router = useRouter()
    const { mobile } = useDisplay()
    const openPlaylist = async(link) => {
        router.push(link)
    }

    /* Table */
    const loading = ref(false)
    const items = ref([])
    const search = ref("")
    const totalItems = ref(0)

    const uriParams = new URLSearchParams()

    const headers =[
        { title: 'Title', value: 'name' },
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
        const data = await apiFetch(`playlists/?${uriParams}`)
        items.value = data.results
        totalItems.value = data.count
        loading.value = false
    }

    /* Create Playlist */
    const showCreateDialog = ref(false)
    const createDialogLoading = ref(false)
    const playlistName = ref("")
    const createPlaylist = async () => {
        createDialogLoading.value = true
        const results = await apiFetch("playlists/", {
            method: "post",
            body: {
                name: playlistName.value
            }
        })
        router.push(`playlist/${results.id}`)
        createDialogLoading.value = false
        showCreateDialog.value = false;
    }
</script>