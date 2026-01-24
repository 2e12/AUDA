const runtimeConfig = useRuntimeConfig()
let backendUrl = runtimeConfig.public.backendUrl
const apiFetch = $fetch.create({ baseURL: `${backendUrl}/v1/` })
export default apiFetch