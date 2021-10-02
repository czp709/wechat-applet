// pages/dowfile/dowfile.js
let videoAd = null
Page({


  data: {
    url:""
  },


  onLoad: function (options) {
    var that = this
    that.setData({
      url:options.url
    })
    var that = this
    // 在页面onLoad回调事件中创建激励视频广告实例
    if (wx.createRewardedVideoAd) {
      videoAd = wx.createRewardedVideoAd({
        adUnitId: 'adunit-195c975bac4f1b1a'
      })
      videoAd.onLoad(() => {})
      videoAd.onError((err) => {})
      videoAd.onClose((res) => {
        // 用户点击了【关闭广告】按钮
        if (res && res.isEnded) {
          // 正常播放结束，可以下发游戏奖励
          that.download()
        } else {
          // 播放中途退出，不下发游戏奖励
        }
      })
    }
  },
  showAD(){
    var that = this
    wx.showModal({
      title: '下载提示',
      content: '您需要观看一个广告才能下载，是否观看？',
      success (res) {
        if (res.confirm) {
          that.show()
        } else if (res.cancel) {
          console.log('用户点击取消')
        }
      }
    })

  },
  show(){
    if (videoAd) {
      videoAd.show().catch(() => {
        // 失败重试
        videoAd.load()
          .then(() => videoAd.show())
          .catch(err => {
            console.log('激励视频 广告显示失败')
          })
      })
    }
  },
  download: function (e) {
    let that = this
    wx.showLoading({
      title: '正在保存',
    })
    var aa = wx.getFileSystemManager();
    console.log(that.data.url)
    aa.writeFile({
      filePath:wx.env.USER_DATA_PATH+'/test.png',
      data: that.data.url.slice(22),
      encoding:'base64',
      success: res => {
        wx.hideLoading({
          success: (res) => {},
        })
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