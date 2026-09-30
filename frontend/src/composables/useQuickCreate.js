import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

// Ephemeral UI intent: never stored in URL/history, never creates records itself.
const intent = ref(null)
export function requestQuickCreate(kind) { intent.value = kind }
export function clearQuickCreate() { intent.value = null }
export function useQuickCreate(kind, path, open) {
  const route = useRoute()
  watch([intent, () => route.path], ([pending, currentPath]) => {
    if (pending !== kind || currentPath !== path) return
    intent.value = null
    open()
  }, { immediate: true })
}
