<template>
    <v-container class="fill-height justify-center align-center fill-height">
        <v-card title="Import" subtitle="Choose the import source" variant="outlined">
            <v-list>
                <v-list-item prepend-icon="mdi-file" to="import/local" v-ripple>
                    Import Local Audio File
                </v-list-item>
                <v-list-item prepend-icon="mdi-youtube" to="import/youtubeVideo" v-ripple>
                    Import YouTube Video
                </v-list-item>
                <v-list-item prepend-icon="mdi-youtube" to="import/youtubePlaylist" v-ripple>
                    Import YouTube Playlist
                </v-list-item>
            </v-list>
        </v-card>
    </v-container>
</template>
<script setup>

</script>