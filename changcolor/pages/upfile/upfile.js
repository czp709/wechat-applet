// pages/upfile/upfile.js
let i = 0
// 在页面中定义激励视频广告
Page({
  data: {
  tempFilePaths: [],
  flag:true,
  color:""
  },
  colorchange(e){
    let color = e.detail.value;
    console.log(color)
    this.setData({
      color:color
    })
  },
  chosefile(){
    let that = this
    wx.chooseImage({
      count: 1, // 默认9
      sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
      sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
      success: res => {
        console.log(res)
        if(res.tempFiles.size/1024/124>4){
          wx.showToast({
            title: '照片大小不得超过4M',
            duration:2000,
            icon:'none'
          })
          return false
        }else{
          let tempFilePaths = res.tempFilePaths;
          that.setData({
            tempFilePaths: tempFilePaths,
            flag:false
          })
        }
      }
  })
},
  upfile(){
    let that = this
    if(!that.data.tempFilePaths[0]){
      return false
    }
    wx.showLoading({
      title: '上传中',
     })
    wx.uploadFile({
      filePath: that.data.tempFilePaths[0],
      url: 'https://chenzp.ltd/changecolor/file_upload',
      method:'POST',
      name:"file",
      header: {
        'content-type': 'multipart/form-data',
      },
      formData:{
        "color":"text"
      },
      success(res){
        wx.hideLoading()
        let data=JSON.parse(res.data)
        if(that.data.color==="red"){
          i =0
        }
        else if(that.data.color==="blue"){
          i=1
        }
        else{
          i = 2
        }
        let url = 'data:image/png;base64,' + data.data[i]
        wx.navigateTo({
          url: '/pages/dowfile/dowfile?url=' + url
        })
      },
      fail(res){
        wx.hideLoading()
         console.log(res)
      }

    })
  }
})