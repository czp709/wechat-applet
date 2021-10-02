Page({
  data: {
    list:[
      {id:0,url:"/image/16.png",lvjing:"甜薄荷"},
      {id:1,url:"/image/14.png",lvjing:"樱桃布丁"},
      {id:2,url:"/image/13.png",lvjing:"玫瑰初雪"},
      {id:3,url:"/image/17.png",lvjing:"樱红"},
      {id:4,url:"/image/29.png",lvjing:"自然"}
    ],
    color:"white",
    current_tag:null,
    tempFilePaths:"",
    flag:true,
    filter:null,
    urls:[]
  },
// 从相册选择照片
  chosefile(){
    let that = this
    wx.chooseImage({
      count: 1, // 默认9
      sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
      sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
      success: res => {
        wx.showToast({
          title: '正在上传...',
          icon: 'loading',
          mask: true,
          duration: 1000
        })
        let tempFilePaths = res.tempFilePaths;
        that.setData({
          tempFilePaths: tempFilePaths,
          flag:false
        })
        var timestamp = Date.parse(new Date());  
        timestamp = timestamp / 1000; 
        wx.showLoading({
          title: '制作中请稍后',
         })
        wx.uploadFile({
          filePath: that.data.tempFilePaths[0],
          url: 'https://chenzp.ltd/changecolor/file_upload1',
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
            console.log(data)
            let i = 0
            let urls = []
            for(i;i<7;i++){
              let url = 'data:image/png;base64,' + data.data[i]
              if(url===""){
                continue;
              }
              urls.push(url)
            }
            that.setData({
              urls : urls
            })
          },
          fail(res){
            wx.hideLoading()
             console.log(res)
          }
    
        })
      }
    })
  },
// 选择滤镜上传图片到服务器进行修改
  clickedAction: function (responseObject){
    let that = this;
    var id = responseObject.currentTarget.dataset.id;  //获取自定义的ID值 
    var lvjing = this.data.list[id].lvjing
    console.log("current_tag", id)
    let tempFilePath = that.data.urls[id]
    this.setData({
      tempFilePaths:tempFilePath,
      current_tag: id,
      filter : lvjing,
    })

   
  },
// 点击按钮将服务器返回的图片进行保存
  download: function (e) {
    let that = this
    var aa = wx.getFileSystemManager();
    console.log(that.data.tempFilePaths)
    aa.writeFile({
      filePath:wx.env.USER_DATA_PATH+'/test.png',
      data: that.data.tempFilePaths.slice(22),
      encoding:'base64',
      success: res => {
        wx.saveImageToPhotosAlbum({
          filePath: wx.env.USER_DATA_PATH + '/test.png',
          success: function (res) {
            wx.showToast({
              title: '保存成功',
            })
          },
          fail: function (err) {
            console.log(err)
          }
        })
        console.log(res)
      }, fail: err => {
        console.log(err)
      }
    })
  },

})