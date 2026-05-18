import { onBeforeRouteLeave } from 'vue-router'
import { onBeforeUnmount, onMounted } from 'vue'
import { ElMessageBox } from 'element-plus'

export function useUnsavedGuard(isDirty) {
    const beforeUnloadHandler = (e) => {
        if (isDirty.value) {
            e.preventDefault()
            e.returnValue = ''
        }
    }

    onMounted(() => {
        window.addEventListener('beforeunload', beforeUnloadHandler)
    })

    onBeforeUnmount(() => {
        window.removeEventListener('beforeunload', beforeUnloadHandler)
    })

    onBeforeRouteLeave(async () => {
        if (!isDirty.value) return true
        try {
            await ElMessageBox.confirm('当前修改尚未保存，确定要离开吗？', '提示', {
                confirmButtonText: '离开',
                cancelButtonText: '取消',
                type: 'warning'
            })
            return true
        } catch {
            return false
        }
    })
}
