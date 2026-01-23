import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000
})

export interface Product {
  name: string
  category: string
  brand: string
  material: string
  size: string
  color: string
  targetGroup: string
  imageUrl?: string
}

export interface DraftRequest {
  products: Product[]
  saveToAsset: boolean
}

export interface DraftResponse {
  jobId: string
}

export interface JobStatus {
  total: number
  finished: number
  status: 'PENDING' | 'PROCESSING' | 'DONE' | 'FAILED'
  results: Array<{
    productId: string
    title: string
    sellingPoints: string
    imageUrl: string
  }>
}

// 图片分析相关接口
export interface ImageAnalysisResult {
  status: 'success' | 'error'
  message: string
  data: {
    product_info: {
      name: string
      category: string
      brand: string
      material: string
      size: string
      color: string
      targetGroup: string
      imageUrl: string
    }
    analysis: {
      selling_points: string[]
      keywords: string[]
      description: string
      target_audience: string
    }
    generated_content: {
      title: string
      selling_points: string
      brand: string
      material: string
      size: string
      color: string
      target_group: string
    }
  }
}

export const uploadApi = {
  // 上传图片到 Cloudinary
  uploadImage: async (file: File): Promise<string> => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('upload_preset', 'ecommerce-draft')
    
    const response = await axios.post(
      `https://api.cloudinary.com/v1_1/${import.meta.env.VITE_CLOUDINARY_CLOUD_NAME}/image/upload`,
      formData
    )
    return response.data.secure_url
  },

  // 创建草稿任务
  createDraft: async (data: DraftRequest): Promise<DraftResponse> => {
    const response = await api.post('/draft/batch', data)
    return response.data
  },

  // 获取任务状态
  getJobStatus: async (jobId: string): Promise<JobStatus> => {
    const response = await api.get(`/draft/status/${jobId}`)
    return response.data
  },

  // 下载 ZIP 包
  downloadZip: async (imageUrls: string[]): Promise<Blob> => {
    const response = await api.post('/download-zip', { imageUrls }, {
      responseType: 'blob'
    })
    return response.data
  },

  // 图片分析相关API
  analyzeImageFromUrl: async (imageUrl: string): Promise<ImageAnalysisResult> => {
    const response = await api.post('/image-analysis/analyze-from-url', { image_url: imageUrl })
    return response.data
  },

  analyzeImageFromUpload: async (file: File): Promise<ImageAnalysisResult> => {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await api.post('/image-analysis/analyze-from-upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  },

  uploadImageToServer: async (file: File): Promise<string> => {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await api.post('/image-analysis/upload-image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data.image_url
  }
}