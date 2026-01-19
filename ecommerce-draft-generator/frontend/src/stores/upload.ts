import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { uploadApi, Product, DraftRequest } from '@/api'

export const useUploadStore = defineStore('upload', () => {
  const products = ref<Product[]>([])
  const saveToAsset = ref(false)
  const uploadingImages = ref(false)
  const uploadProgress = ref(0)
  const jobId = ref<string | null>(null)
  const jobStatus = ref<any>(null)
  const pollingInterval = ref<number | null>(null)

  const hasProducts = computed(() => products.value.length > 0)
  const isProcessing = computed(() => jobStatus.value?.status === 'PROCESSING')
  const isDone = computed(() => jobStatus.value?.status === 'DONE')

  // 解析 Excel 文件
  const parseExcel = async (file: File) => {
    const XLSX = await import('xlsx')
    const data = await file.arrayBuffer()
    const workbook = XLSX.read(data)
    const sheetName = workbook.SheetNames[0]
    const worksheet = workbook.Sheets[sheetName]
    const jsonData = XLSX.utils.sheet_to_json(worksheet)

    const requiredFields = ['name', 'category', 'brand', 'material', 'size', 'color', 'targetGroup']
    const validProducts: Product[] = []

    for (const row of jsonData) {
      const product: any = {}
      let isValid = true

      for (const field of requiredFields) {
        if (!row[field as keyof typeof row]) {
          isValid = false
          break
        }
        product[field] = String(row[field as keyof typeof row])
      }

      if (isValid) {
        validProducts.push(product)
      }
    }

    products.value = validProducts
  }

  // 上传图片
  const uploadImages = async (files: File[]) => {
    uploadingImages.value = true
    uploadProgress.value = 0

    try {
      const uploadedUrls: string[] = []
      
      for (let i = 0; i < files.length; i++) {
        const file = files[i]
        // 压缩图片
        const compressedFile = await compressImage(file)
        const url = await uploadApi.uploadImage(compressedFile)
        uploadedUrls.push(url)
        uploadProgress.value = ((i + 1) / files.length) * 100
      }

      // 将图片 URL 分配给产品
      products.value.forEach((product, index) => {
        if (uploadedUrls[index]) {
          product.imageUrl = uploadedUrls[index]
        }
      })
    } finally {
      uploadingImages.value = false
    }
  }

  // 压缩图片
  const compressImage = (file: File): Promise<File> => {
    return new Promise((resolve) => {
      const reader = new FileReader()
      reader.onload = (e) => {
        const img = new Image()
        img.onload = () => {
          const canvas = document.createElement('canvas')
          const ctx = canvas.getContext('2d')!
          
          // 压缩到 800px 宽
          const maxWidth = 800
          const scale = maxWidth / img.width
          canvas.width = maxWidth
          canvas.height = img.height * scale

          ctx.drawImage(img, 0, 0, canvas.width, canvas.height)
          
          canvas.toBlob((blob) => {
            if (blob && blob.size < 200 * 1024) {
              resolve(new File([blob], file.name, { type: 'image/webp' }))
            } else {
              // 如果仍然大于 200KB，继续压缩
              canvas.toBlob((compressedBlob) => {
                resolve(new File([compressedBlob!], file.name, { type: 'image/webp' }))
              }, 'image/webp', 0.8)
            }
          }, 'image/webp', 0.9)
        }
        img.src = e.target?.result as string
      }
      reader.readAsDataURL(file)
    })
  }

  // 生成草稿
  const generateDraft = async () => {
    const request: DraftRequest = {
      products: products.value,
      saveToAsset: saveToAsset.value
    }

    const response = await uploadApi.createDraft(request)
    jobId.value = response.jobId
    startPolling()
  }

  // 轮询任务状态
  const startPolling = () => {
    pollingInterval.value = window.setInterval(async () => {
      if (!jobId.value) return

      try {
        const status = await uploadApi.getJobStatus(jobId.value)
        jobStatus.value = status

        if (status.status === 'DONE' || status.status === 'FAILED') {
          stopPolling()
        }
      } catch (error) {
        console.error('轮询失败:', error)
        stopPolling()
      }
    }, 1000)
  }

  // 停止轮询
  const stopPolling = () => {
    if (pollingInterval.value) {
      clearInterval(pollingInterval.value)
      pollingInterval.value = null
    }
  }

  // 下载 ZIP
  const downloadZip = async () => {
    if (!jobStatus.value?.results) return

    const imageUrls = jobStatus.value.results.map((r: any) => r.imageUrl)
    const blob = await uploadApi.downloadZip(imageUrls)
    
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `商品草稿_${new Date().toISOString().slice(0, 10)}.zip`
    a.click()
    URL.revokeObjectURL(url)
  }

  // 重置状态
  const reset = () => {
    products.value = []
    saveToAsset.value = false
    jobId.value = null
    jobStatus.value = null
    stopPolling()
  }

  return {
    products,
    saveToAsset,
    uploadingImages,
    uploadProgress,
    jobId,
    jobStatus,
    hasProducts,
    isProcessing,
    isDone,
    parseExcel,
    uploadImages,
    generateDraft,
    downloadZip,
    reset
  }
})