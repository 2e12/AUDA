<template>
    <v-container class="pa-0">
        <v-row class="align-center justify-center">
            <v-col>
                <v-row class="text-center align-center justify-center mt-1"><span v-if="store.currentlyPlaying">{{ store.currentlyPlaying.name  }}</span><span v-else>No Track Playing</span></v-row>
                <v-row>
                    <v-col cols="2" class="text-center">{{ timeLabel }}</v-col>
                    <v-col><v-slider color="deep-purple-accent-1" hide-details :disabled="!audioLoaded" @end="setTime" v-model="currentTime" class="mx-8" :max="duration"></v-slider></v-col>
                    <v-col cols="2" class="text-center">{{ durationLabel }}</v-col>
                </v-row>
            </v-col>
            <v-col cols="12" sm="4" class="align-center justify-center d-flex">
                <v-btn :disabled="!audioLoaded" @click="playlistDialog=store.currentlyPlaying" class="mr-2" icon="mdi-playlist-plus" size="small" variant="plain"></v-btn>
                <v-btn :disabled="!audioLoaded" class="mx-2" icon="mdi-skip-previous" variant="outlined" size="small"></v-btn>
                <v-btn :disabled="!audioLoaded" @click="togglePlay" v-if="!isPlaying" class="mx-2" icon="mdi-play" variant="outlined"></v-btn>
                <v-btn :disabled="!audioLoaded" @click="togglePlay" v-if="isPlaying" class="mx-2" icon="mdi-pause" variant="outlined"></v-btn>
                <v-btn :disabled="!store.hasNextTrack" @click="store.playNext" class="mx-2" icon="mdi-skip-next" variant="outlined" size="small"></v-btn>
                <v-btn class="ml-2" to="/queue" icon="mdi-tray-full" size="small" variant="plain"></v-btn>
            </v-col>
        </v-row>
        <v-dialog
            v-model="playlistDialog"
            max-width="500"
            :fullscreen="mobile"
        >
            <add-song-to-playlist @close="playlistDialog=false" :track="playlistDialog"></add-song-to-playlist>
        </v-dialog>
    </v-container>
</template>
<script setup>
    /* Playlist add */
    const { mobile } = useDisplay()
    const playlistDialog = ref(false)

    /* Player */
    const store = usePlayerStore()
    store.$subscribe((mutation, state) => {
        isPlaying.value = true
        setAudio(state.audioUrl)
        audio.currentTime = state.duration
    })
    const audioLoaded = ref(false)
    let audioUrl
    const isPlaying = ref(false)
    const duration = ref(0)
    const durationLabel = ref("00:00")
    const currentTime = ref(0)
    const timeLabel = ref("00:00")
    let audio = new Audio()
    const timeToLabel = (s) => {
        const hours = Math.floor(s / 3600);
        const minutes = Math.floor((s % 3600) / 60);
        const seconds = Math.floor(s % 60);

        return new Intl.DurationFormat("de-DE", { style: "digital" })
            .format({ hours, minutes, seconds });
    };
    const updateTime = () => {
        currentTime.value = audio.currentTime
        timeLabel.value = timeToLabel(currentTime.value)
    }
    const setTime = (value) => {
        audio.currentTime = currentTime.value
    }
    const setAudio = (audioUrl) => {
        audioLoaded.value = false
        audio.removeEventListener("pause", pause)
        audio.pause()
        audio = new Audio(audioUrl)
        audio.autoplay = false
        audio.addEventListener("canplay", (event) => {
            duration.value = audio.duration
            durationLabel.value = timeToLabel(duration.value)
            audioLoaded.value = true
            if(isPlaying.value) {
                audio.play()
            } else {
                audio.pause()
            }
        });
        audio.addEventListener("timeupdate", updateTime)
        audio.addEventListener("ended", (event) => {
            currentTime.value = 0
            if (!store.playNext()) {
                isPlaying.value = false
            }
        })
        audio.addEventListener("pause", pause)
        audio.addEventListener("play", (event) => {
            isPlaying.value = true
        })
        audio.addEventListener("error", (event) => {
            store.playNext()
        })
        return audio
    }
    const togglePlay = () => {
        isPlaying.value = !isPlaying.value
        if(isPlaying.value) {
            audio.play()
        } else {
            audio.pause()
        }
    }
    const pause = (event) => {
        isPlaying.value = false
    }
</script>