import apiFetch from '~/fetch';
const runtimeConfig = useRuntimeConfig()
let backendUrl = runtimeConfig.public.backendUrl
export const usePlayerStore = defineStore('playerStore', {
  state: () => ({
    currentlyPlaying: null,
    audioUrl: null,
    queue: [],
    duration: 0,
  }),
  getters: {
    hasNextTrack: (state) => state.queue.length,
  },
  actions: {
    async clear() {
      this.queue = []
      this.currentlyPlaying = null
      this.audioUrl = null
      this.duration = 0
    },
    async addListToQueue(ids) {
      await this.clear()
      for (const id of ids) {
        if (!this.currentlyPlaying) {
          await this.play(id)
        } else {
          this.addToQueue(id)
        }
      }
    },
    async addToQueue(id) {
      if (!this.currentlyPlaying) {
        return this.play(id)
      }
      const data = await apiFetch("/tracks/" + id + "/")
      this.queue.push({
        data: data,
        audioUrl: `${backendUrl}/library/stream/${id}`,
      })
    },
    async playNext() {
      if (this.queue.length) {
        const next = this.queue.shift()
        this.currentlyPlaying = next.data
        this.audioUrl =  next.audioUrl
        return true
      }
      return false
    },
    async play (id, duration = 0) {
      const data = await apiFetch("tracks/" + id + "/")
      this.queue = []
      this.currentlyPlaying = data
      this.audioUrl = `${backendUrl}/library/stream/${id}`,
      this.duration = duration
    },
  },
})
