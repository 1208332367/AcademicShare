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
					<view class="title">身份认证</view>
				<!-- #endif--> 
				<view class="body">	
					<input class="text" placeholder="华师大学工号" @input="getStuID"/>
					<input class="text" type="password" placeholder="华师大公共数据库密码" @input="getStuPassword"/>
					<view class="extra">
						<image src="../../../static/myinfo/hint.png" mode="aspectFit"></image>
						<view class="right">
							仅验证身份，不保存密码
						</view>
					</view>
					<button class="submit" @click="submit">
						立即认证
					</button>		
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
				stuID: '',
				stuPassword: ''
			}
		},
		onLoad() {
			this.app_platform = App.globalData.app_platform
			uni.$emit('disableInput', true)
		},	
		onShow() {
			App.checkLoginStatus()
		},	
		methods: {
			getStuID:function(e){
				this.stuID = e.target.value			
			},
			getStuPassword:function(e){
				this.stuPassword = e.target.value			
			},
			submit:function(){
				if(!this.stuID.length){
					App.errorToast('学工号不能为空')
					return
				}
				if(!this.stuPassword.length){
					App.errorToast('密码不能为空')
					return
				}
				var that = this
				try{
					var userInfo = uni.getStorageSync('userInfo')
					uni.request({
						url: App.globalData.rootUrl + 'user/authentication',
						data: {
							UserID: userInfo.UserID,
							studentID: that.stuID,
							studentPassword: that.stuPassword
						},
						method:'POST',
						header:{
							'content-type': 'application/x-www-form-urlencoded'
						},
						success: (res) => {
							if(res.data.code)
								App.errorToast(res.data.msg)
							else{
								userInfo['role'] = 2
								try{
									userInfo['cachetimestamp'] = App.getCurrentSecond()
									uni.setStorageSync("userInfo", userInfo)
								}catch(e){
									
								}
								uni.$emit('login', userInfo)
								App.successToast("认证成功")
								setTimeout(function(){
								  uni.navigateBack({
								  	delta: 1
								  })
								}, 500)
							}
						},
						fail: (res) => {
							App.requestFailToast()
						}
					})
				}catch(e){
					
				}		
			},
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
		margin-top:30px;
		overflow: hidden;
		height:300px;
		/*border: #000000 solid 2rpx;*/
		display: flex;
		flex-direction: column;
		align-items: center;
	}
	@media only screen and (min-width: 1029px){
		.body{
			margin-top:50px;
		}
	}
	.body .text{
		margin-top: 20px;
		width:70%;
		height: 50px;
		font-size: small;
		border: #3F536E solid 2rpx;
		display: flex;
		align-items: center;
		color: #000000;
		border-radius: 10rpx 10rpx 10rpx 10rpx;
		padding-left:10rpx;
	}
	.submit{
		width:71%;
		height: 50px;
		margin-top:50px;
		background-color: #3249F8;
		display: flex;
		align-items: center;
		justify-content: center;
		color: #FFFFFF;
	}
	.body .extra{
		width:70%;
		height: 50px;
		font-size: small;
		display: flex;
		align-items: center;
		color: #AAAAAA;
	}
	.body .extra image{
		width: 40rpx;
		height: 100%;
	}
	.body .extra view{
		margin: 10rpx;
	}
	@media only screen and (min-width: 1029px){
		.body .extra view{
			margin: 5px;
		}
	}
</style>
