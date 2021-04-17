<template>
	<view>
		<view class="page">
			<view class="main">
				<!--
				<view v-if="app_platform!='PC'" style="width: 100%;">
					<AppHeader></AppHeader>
				</view>
				
				<view v-if="app_platform!='PC'" style="height: 40px;">
				</view>
				<view v-else  style="height: 50px;">
				</view>
				-->
				<!-- #ifdef H5 -->
					<view class="title">资源上传</view>
				<!-- #endif--> 
				<view class="body">
					
					<view class="inputText">
						<view class="left">
							资源标题：
						</view>
						<input class="text" placeholder="不超过10字" maxlength="10" @input="getInputTitle"/>
					</view>
					
					<view class="inputText" style="height: 70px;">
						<view class="left">
							资源文件：
						</view>
						<view class="text" style="border: #FFFFFF solid 2px;" >
							<!-- #ifdef H5-->
							<uni-file-picker :file-extname="['zip','rar']" limit="1" file-mediatype="all" title="zip/rar文件, 不超过10M" @success="uploadSuccess" @fail="uploadFail" @delete="deleteFile"></uni-file-picker>
							<!-- #endif -->
							<!-- #ifndef H5 -->
							<view style="color:red;">该平台无法上传文件</view>
							<!-- #endif -->
						</view>
					</view>
					
					<view class="inputText">
						<view class="left">
							学科大类：
						</view>
						<view class="text" style="border: #FFFFFF solid 2px;">
							<view class="my_picker">
								<picker  @change="bindProfessionsPickerChange" :value="professions_index" :range="professions" >
									<view class="uni-input">{{professions[professions_index]}}</view>
								</picker>
								<image src="../../static/upload/down.png" mode="aspectFit"></image>
							</view>
						</view>
					</view>
					
					<view class="inputText">
						<view class="left">
							访问权限：
						</view>
						<view class="text" style="border: #FFFFFF solid 2px;">
							<view class="my_picker">
								<picker  @change="bindVisitsPickerChange" :value="visits_index" :range="visits" >
									<view class="uni-input">{{visits[visits_index]}}</view>
								</picker>
								<image src="../../static/upload/down.png" mode="aspectFit"></image>
							</view>
						</view>
					</view>
					
					<view class="inputText" style="margin-top: 20px;">
						<view class="left" style="padding-top: 7px; height:100%;display:flex;align-items: flex-start;">
							资源简介：
						</view>
						<textarea class="text" style="padding-top:5px;align-items: flex-start;height: 90%;" placeholder="不超过200字" maxlength="200" @input="getInputIntro"/>
					</view>
				
					<view class="submit">
						<button @click="submit">
							提交
						</button>
					</view>
				</view>		
					
			</view>
			
		</view>	
		<!-- #ifdef H5 -->
			<Footer v-if="app_platform=='PC'"></Footer>
		<!-- #endif-->
	</view>
</template>

<script>
	let App = getApp()
	export default {
		data() {
			return {
				app_platform: 'PC',
				professions_index: 0,
				visits_index: 0,
				professions: [],
				visits:[
					"无限制", "仅校内"
				],
				title: '',
				intro: '',
				filePath: '',	
				extname: '',
			}
		},
		onLoad() {
			this.app_platform = App.globalData.app_platform
			this.getProfession()
			uni.$emit('disableInput', true)
		},	
		onShow() {
			App.checkLoginStatus()
		},
		methods: {
			bindProfessionsPickerChange: function(e) {
			    //console.log('picker发送选择改变，携带值为', e.target.value)
			    this.professions_index = e.target.value
			},
			bindVisitsPickerChange: function(e) {
			    //console.log('picker发送选择改变，携带值为', e.target.value)
			    this.visits_index = e.target.value
			},
			getProfession: function(){
				var that = this
				uni.request({
					url: App.globalData.rootUrl + 'profession/listProfession',
					data: {
					},
					method:'POST',
					header:{
						'content-type': 'application/x-www-form-urlencoded'
					},
					success: (res) => {
						if(res.data.code)
							App.errorToast(res.data.msg)
						else{
							var arr = res.data.data	
							for(var i = 0; i < arr.length; i++)
								that.professions.push(arr[i].name)
						}
					},
					fail: (res) => {
						App.requestFailToast()
					}
				})
			},
			getInputTitle: function(e){
				this.title = e.target.value
			},
			getInputIntro: function(e){
				this.intro = e.target.value
			},
			uploadSuccess:function(e){
				//getApp().successToast("文件上传成功")
				this.filePath = e.tempFilePaths[0]
				this.extname = e.tempFiles[0].extname
			},
			uploadFail:function(e){
				getApp().errorToast("文件上传失败")
				this.filePath = ''
				this.extname = ''
			},		
			deleteFile:function(){
				this.filePath = ''
				this.extname = ''
			},
			submit: function(){
				if(!this.title.length){
					App.errorToast('标题不能为空')
					return
				}
				if(!this.intro.length){
					App.errorToast('简介不能为空')
					return
				}
				if(!this.filePath.length){
					App.errorToast('文件不能为空')
					return
				}
				var that = this
				try{
					let current_userinfo = uni.getStorageSync('userInfo')
					if(current_userinfo['role'] < 2 && parseInt(that.visits_index) == 1){
						App.errorToast('游客无法限制资源权限')
						return
					}
					uni.showModal({
						showCancel: true,
						title: '确定提交？',
						success: (res) =>  {
							if(res.confirm){
								uni.showLoading({
									title: '正在提交...'
								})
								uni.uploadFile({
									url: getApp().globalData.rootUrl + 'resource/uploadFile',
									filePath: that.filePath,
									name: 'file',
									formData: {
										'UserID': current_userinfo.UserID,
										'title': that.title,
										'resource_intro': that.intro,
										'visitCtrl': parseInt(that.visits_index) ^ 1,
										'ProfessionID': parseInt(that.professions_index) + 1,
										'extname': that.extname
									},			
									success: (res) => {
										var new_res = JSON.parse(res.data)
										if(new_res.code)
											getApp().errorToast(new_res.msg)
										else{
											setTimeout(function(){
											  uni.hideLoading()
											  getApp().successToast("提交成功")
											}, 1000)
											
											setTimeout(function(){
											  uni.switchTab({
													url: '/pages/index/index'
											  })
											}, 2000)
										}
									},
									fail: (res) => {
										uni.hideLoading()
										getApp().requestFailToast()
									}
								})
							}
						}
					})			
				}catch(e){
					
				}	
			}
		}
	}
</script>

<style>
	.title{
		font-weight: bold;
		font-size: large;
		display: flex;
		align-items: center;
		justify-content: center;
		width: 100%;
		height: 100px;
	}
	.body{
		width: 95%;
		margin-top:20px;
		overflow: hidden;
	}
	@media only screen and (min-width: 1029px){
		.body{
			margin-top:30px;
		}
	}
	.inputText{
		width: 100%;
		height: 60px;
		/*border: #000000 solid 2px;*/
		display: flex;
		align-items: center;
		justify-content: center;
	}
	.inputText .left{
		/*width: 20%;*/
		margin-left: 20rpx;
	}
	.inputText .text .upload_file{
		color: #00C7FF;
		font-weight: bold;
	}
	.inputText .text{
		width:70%;
		height: 60%;
		font-size: small;
		border: #3F536E solid 2rpx;
		display: flex;
		align-items: center;
		color: #000000;
		border-radius: 10rpx 10rpx 10rpx 10rpx;
		margin-left: 10rpx;
		padding-left:10rpx;
	}
	.inputText .text .my_picker {
		height: 100%;
		display: flex;
		align-items: center;
	}
	.inputText .text .my_picker view{
		padding-right: 30rpx;
		
		z-index: 999;
	}
	.inputText .text .my_picker image{
		height: 100%;
		width: 50rpx;
		margin-left: -30rpx;
		z-index:-1;
		margin-top: 1px;
	}
	.submit{
		margin-top: 50px;
		width: 100%;
	}
	.submit button{
		width: 50%;
		background-color: #3249F8;
		color: #FFFFFF;
	}
</style>
