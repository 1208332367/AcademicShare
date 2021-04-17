<script>
	export default {
		globalData: {
			app_platform: 'PC',
			systemInfo: uni.getSystemInfoSync(),
			domain: 'https://share.ecnucs.club:8131/',
			rootUrl: 'https://share.ecnucs.club:8131/service/',
		},
		onLaunch: function() {
			console.log('App Launch')
			var windowWidth = this.globalData.systemInfo.screenWidth
				
			// #ifdef H5
			if (windowWidth < 1028) {
			    this.globalData.app_platform='phone' 
			}
			else{
				uni.hideTabBar()	
			}
			// #endif
				
			// #ifndef H5
			//plus.navigator.setFullscreen(false);
			this.globalData.app_platform='app' 
			console.log(windowWidth)
			// #endif	
			
		},	
		onShow: function() {
			console.log('App Show')
		},
		onHide: function() {
			console.log('App Hide')
		},
		methods:{
			getCurrentSecond:function(){
				//console.log(new Date().getTime() / 1000)
				return new Date().getTime() / 1000
			},
			checkLoginStatus:function(){
				try{
					let current_userinfo = uni.getStorageSync('userInfo')
					//console.log(current_userinfo)
					let current_stamp = new Date().getTime() / 1000
					//console.log("-----")
					//console.log(current_userinfo['cachetimestamp'].toString())
					//console.log(current_stamp.toString())
					if((current_stamp - current_userinfo['cachetimestamp'] > (3600 * 72)) || current_userinfo == 'empty' || !current_userinfo){
						uni.$emit('login', 'empty')
						uni.setStorageSync("userInfo", 'empty')
						uni.redirectTo({
							url: '/pages/login/login'
						})
					}
					else{
						current_userinfo['cachetimestamp'] = new Date().getTime() / 1000
						uni.setStorageSync("userInfo", current_userinfo)
						uni.$emit('login', current_userinfo)
					}
				}catch(e){
					console.log(e)
					uni.$emit('login', 'empty')
					try{
						uni.setStorageSync("userInfo", 'empty')
						uni.redirectTo({
							url: '/pages/login/login'
						})
					}catch(e){
						//console.log(e)
					}
				}	
			},
			requestFailToast:function(){
				uni.showToast({
					icon: 'none',
					title: '服务器无响应',
					duration: 1500
				})
			},
			errorToast:function(errMsg){
				uni.showToast({
					icon: 'none',
					title: errMsg,
					duration: 1500
				})
			},
			successToast:function(msg){
				uni.showToast({
					icon: 'success',
					title: msg,
					duration: 1500
				})
			},
			getDateFromCtime:function(ctime){
				return ctime.split("T")[0]
			},
			getFixedScore:function(score){
				return score > 0? score.toFixed(1): "无"
			},
			getFixedFileSize:function(size){
				if(size > 1024){
					return (size / 1024.0).toFixed(2).toString() + "MB"
				}
				else{
					if(size >= 0.01){
						return size.toFixed(2).toString() + "KB"
					}
					else{
						return (1024.0 * size).toFixed(2).toString() + "B"
					}
				}
			},
		}
	}
</script>

<style>
	/*每个页面公共css */
	.page{ 
		padding: 5rpx;
		padding-top:0;
		font-size: 14px;
		/*border: #000000 solid 2px;*/
		display: flex;
		justify-content: center;
		height: 580px;
	}
	
	.main{
		width: 100%;
		/*border: #000000 solid 2px;*/
		height:100%;
		display: flex;
		flex-direction: column;
		align-items: center;
	}
	
	@media only screen and (min-width: 1029px){
		.main{
			width:63%;
			/*border: #C0C4CC solid 3px;*/
			margin-top: 10px;
		}
	}
	
</style>
