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
					<view class="title">个人中心</view>
				<!-- #endif--> 
				
				<view class="body">
				
					<view class="user">
						<image src="../../static/index/avatar.png" mode="aspectFit" @click="changeAvatar"></image>
						<view class="userinfo">
							<view class="nickname">
								<block v-if="!clickModifyNickName">
									<view class="nickname_text">{{userInfo.nickName}}</view>
									<image src="../../static/myinfo/modify_name.png" mode="aspectFit" @click="modifyNickName"></image>
								</block>
								<block v-else>
									<input class="nickname_input" :placeholder="userInfo.nickName" maxlength="10" @input="getNewNickName"/>
									<image src="../../static/myinfo/confirm.png" mode="aspectFit" @click="submitNickName"></image>
									<image src="../../static/myinfo/cancel.png" mode="aspectFit" @click="cancelModifyNickName"></image>
								</block>
							</view>
							<view class="account">
								<view class="number">
									账号：{{userInfo.account}}
								</view>
								<view v-if="userInfo.role<2" class="authentication" @click="goToAuthentication">
									点击认证
								</view>
								<view v-else class="authentication">
									已认证
								</view>
							</view>
						</view>
					</view>
					
					<view class="navigation_list">
						<view class="navigate" @click="goToModifyPassword">
							<view>密码修改</view>
							<image src="../../static/myinfo/right.png" mode="aspectFit"></image>
						</view>
						<view class="navigate" @click="goToMyFavor">
							<view>我的收藏</view>
							<image src="../../static/myinfo/right.png" mode="aspectFit"></image>
						</view>
						<view class="navigate" @click="goToMyUpload">
							<view>我的上传</view>
							<image src="../../static/myinfo/right.png" mode="aspectFit"></image>
						</view>
						<view class="navigate" style="border-bottom: #DDDDDD solid 2px;" @click="goToMyDownload">
							<view>我的下载</view>
							<image src="../../static/myinfo/right.png" mode="aspectFit"></image>
						</view>
					</view>
					
					<view class="logout" @click="logout">
						<button>
							退出登录
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
				userInfo: {
					"nickName": "未设置",
					"account": "未设置",
					"role": 1
				},
				clickModifyNickName: false,
				newNickName: '',
				islegalNewNickName: false
			}
		},		
		onLoad() {
			this.app_platform = App.globalData.app_platform
			uni.$emit('disableInput', true)
		},	
		onShow() {
			App.checkLoginStatus()
			try{
				let current_userinfo = uni.getStorageSync('userInfo')
				if(current_userinfo != 'empty'){
					this.userInfo = current_userinfo
				}
			}catch(e){
				
			}
			uni.$on('login',(userInfo)=>{
				if(userInfo != 'empty')
					this.userInfo = userInfo;  
				else
					this.userInfo = {
						"nickName": "未设置",
						"account": "未设置",
						"role": 1
					}
			})		
		},	
		methods: {
			reset:function(){
				this.clickModifyNickName = false
				this.newNickName = ''
				this.islegalNewNickName = false
			},
			changeAvatar:function(){
				App.errorToast('暂不支持更换头像')
			},
			goToAuthentication:function(){
				uni.navigateTo({
					url:"./authentication/authentication"
				})
			},
			goToModifyPassword:function(){
				uni.navigateTo({
					url:"./modifyPassword/modifyPassword"
				})
			},
			goToMyFavor:function(){
				uni.navigateTo({
					url:"./myFavor/myFavor"
				})
			},
			goToMyUpload:function(){
				uni.navigateTo({
					url:"./myUpload/myUpload"
				})
			},
			goToMyDownload:function(){
				uni.navigateTo({
					url:"./myDownload/myDownload"
				})
			},
			logout:function(){
				uni.showModal({
					showCancel: true,
					title: '确定退出登录？',
					success: (res) =>  {
						if(res.confirm){
							try{
								uni.setStorageSync("userInfo", 'empty')
							}catch(e){
								App.errorToast("退出登录失败")
							}
							uni.$emit('login', 'empty')
							this.userInfo = {
								"nickName": "未设置",
								"account": "未设置",
								"role": 1
							}
							uni.redirectTo({
								url: '/pages/login/login'
							})
						}
					}
				})						
			},
			getNewNickName:function(e){
				this.newNickName = e.target.value
				if(!e.target.value.length)
					return
				var re = /^[\u4e00-\u9fa5a-z]+$/gi;
				if(!re.test(e.target.value)){
					App.errorToast('请输入汉字或字母')
					this.islegalNewNickName = false
					return
				}
				this.islegalNewNickName = true
			},
			modifyNickName:function(){
				this.clickModifyNickName = true
			},
			submitNickName:function(){	
				if(!this.newNickName.length){
					App.errorToast('昵称不能为空')
					return
				}
				if(this.newNickName == this.userInfo.nickName){
					App.errorToast('昵称未修改')
					return
				}
				if(this.newNickName.length > 10){
					App.errorToast('昵称必须在10字以内')
					return
				}
				if(!this.islegalNewNickName){
					App.errorToast('昵称只能为汉字、字母')
					return
				}
				var that = this
				try{
					var userInfo = uni.getStorageSync('userInfo')
					uni.request({
						url: App.globalData.rootUrl + 'user/modifyNickname',
						data: {
							nickName: that.newNickName,
							UserID: userInfo.UserID
						},
						method:'POST',
						header:{
							'content-type': 'application/x-www-form-urlencoded'
						},
						success: (res) => {
							if(res.data.code)
								App.errorToast(res.data.msg)
							else{
								userInfo["nickName"] = that.newNickName
								try{
									userInfo['cachetimestamp'] = App.getCurrentSecond()
									uni.setStorageSync("userInfo", userInfo)
								}catch(e){
									
								}
								uni.$emit('login', userInfo)
								App.successToast("昵称修改成功")
								this.reset()
							}
						},
						fail: (res) => {
							App.requestFailToast()
						}
					})
				}catch(e){
					
				}		
			},
			cancelModifyNickName:function(){
				this.reset()
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
			margin-top:0px;
		}
	}
	.user{
		display: flex;
		height: 70px;
		/*border: #000000 solid 2rpx;*/
	}
	.user image{
		width: 180rpx;
		height: 100%;
	}
	.user .userinfo{
		width: 70%;
	}
	.user .userinfo .nickname{
		display: flex;
		height: 48%;
		width: 100%;
		align-items: flex-end;
		/*border: #000000 solid 2rpx;*/
		font-size: 120%;
		font-weight: bold;
	}
	.user .userinfo .nickname .nickname_text{
		overflow: auto;
		max-width: 90%;
		height: 100%;
		white-space:nowrap;
		display: flex;
		align-items: flex-end;
	}
	.user .userinfo .nickname .nickname_input{
		overflow: auto;
		max-width: 90%;
		height: 80%;
		font-size: 80%;
		white-space:nowrap;
		display: flex;
		align-items: flex-end;
		border: #3F536E solid 1px;
		border-radius: 5px 5px 5px 5px;
		font-weight: normal;
	}
	.user .userinfo .nickname image{
		width: 40rpx;
		height: 60%;
		display: flex;
		align-items: flex-end;
		/*border: #000000 solid 2rpx;*/
		margin-left: 10rpx;
	}
	@media only screen and (min-width: 1029px){
		.user .userinfo image{
			width: 25px;	
		}
	}
	.user .userinfo .account{
		display: flex;
		align-items: center;
		height: 48%;
		font-size: 90%;
		/*border: #000000 solid 2rpx;*/
		color: #101010;
	}
	.user .userinfo .account .authentication{
		margin-left: 20rpx;
		border: #BBBBBB solid 2rpx;
		border-radius: 20rpx 20rpx 20rpx 20rpx;
		padding: 5rpx;
		padding-left: 10rpx;
		padding-right: 10rpx;
		font-size: 90%;
	}
	.navigation_list{
		margin-top:50px;
		width: 100%;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}
	.navigation_list .navigate{
		width: 85%;
		height: 40px;
		display: flex;
		border-top: #DDDDDD solid 2px;
		align-items: center;
		justify-content: space-between;
		font-size: 110%;
		padding: 15rpx;
	}
	@media only screen and (min-width: 1029px){
		.navigation_list .navigate{
			width: 90%;
		}
	}
	.navigation_list .navigate image{
		height: 100%;
		width: 50rpx;
	}
	.logout{
		margin-top: 50px;
		width: 100%;
	}
	.logout button{
		width: 50%;
		background-color: #3249F8;
		color: #FFFFFF;
	}
</style>
