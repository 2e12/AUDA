<template>
    <v-app>
      <v-layout>
        <v-app-bar elevation="0" class="border-b-thin" color="deep-purple-darken-4" density="compact">
          <template v-slot:prepend>
            <v-app-bar-nav-icon @click="showNav = !showNav"></v-app-bar-nav-icon>
          </template>
          <v-img
            max-height="18"
            max-width="80"
            src="@/assets/audawhite.svg"
          ></v-img>
          <v-app-bar-title></v-app-bar-title>
        </v-app-bar>
        <v-navigation-drawer v-model="showNav">
          <v-list nav>
            <v-list-subheader>Library</v-list-subheader>
            <v-list-item to="/tracks" prepend-icon="mdi-music" title="Tracks" link></v-list-item>
            <v-list-item to="/playlists" prepend-icon="mdi-playlist-music" title="Playlists" link></v-list-item>
            <v-list-item to="/queue" prepend-icon="mdi-tray-full" title="Queue" link></v-list-item>
            <v-btn class="mt-2" block variant="outlined" prepend-icon="mdi-import" to="/import">Import</v-btn>
          </v-list>
        </v-navigation-drawer>
        <v-main class="fill-height">
          <slot />
        </v-main>
        <v-footer elevation="2" name="footer" class="border-t-thin" color="deep-purple-darken-4" app>
          <Player />        
        </v-footer>
      </v-layout>
    </v-app>

</template>

<script setup>
const showNav = ref(true)
</script>