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
					<view class="title">密码修改</view>
				<!-- #endif--> 
				<view class="body">	
					<input class="text" type="password" placeholder="原密码" maxlength="16" @input="getOldPassword"/>
					<input class="text" type="password" placeholder="新密码,8-16位数字、字母" maxlength="16" @input="getNewPassword"/>
					<input class="text" type="password" placeholder="再次输入新密码" maxlength="16" @input="getConfirmNewPassword"/>
					<button class="submit" @click="submit">
						确认修改
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
				oldPassword: '',
				newPassword: '',
				newConfirmPassword: '',
				islegalOldPassword: false,
				islegalNewPassword: false,
				islegalNewConfirmPassword: false,	
				
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
			getOldPassword:function(e){
				this.oldPassword = e.target.value
				if(!e.target.value.length)
					return
				var re = /^[0-9,a-z]+$/gi;
				if(!re.test(e.target.value)){
					App.errorToast('请输入数字或字母')
					this.islegalOldPassword = false
					return
				}			
				this.islegalOldPassword = true
			},
			getNewPassword:function(e){
				this.newPassword = e.target.value
				if(!e.target.value.length)
					return
				var re = /^[0-9,a-z]+$/gi;
				if(!re.test(e.target.value)){
					App.errorToast('请输入数字或字母')
					this.islegalNewPassword = false
					return
				}		
				this.islegalNewPassword = true
			},
			getConfirmNewPassword:function(e){
				this.newConfirmPassword = e.target.value
				if(!e.target.value.length)
					return
				var re = /^[0-9,a-z]+$/gi;
				if(!re.test(e.target.value)){
					App.errorToast('请输入数字或字母')
					this.islegalNewConfirmPassword = false
					return
				}		
				this.islegalNewConfirmPassword = true
			},
			submit:function(){
				if(!this.oldPassword.length){
					App.errorToast('原密码不能为空')
					return
				}
				if(!this.newPassword.length){
					App.errorToast('新密码不能为空')
					return
				}
				if(!this.newConfirmPassword.length){
					App.errorToast('确认新密码不能为空')
					return
				}
				if(this.oldPassword.length < 8 || this.oldPassword.length > 16){
					App.errorToast('原密码必须为8-16位')
					return
				}
				if(!this.islegalOldPassword){
					App.errorToast('原密码只能为数字、字母')
					return
				}
				if(this.newPassword.length < 8 || this.newPassword.length > 16){
					App.errorToast('新密码必须为8-16位')
					return
				}
				if(!this.islegalNewPassword){
					App.errorToast('新密码只能为数字、字母')
					return
				}
				if(this.newPassword != this.newConfirmPassword){
					App.errorToast('两次输入的新密码不一致')
					return
				}
				var that = this	
				try{
					var userInfo = uni.getStorageSync('userInfo')
					uni.request({
						url: App.globalData.rootUrl + 'user/modifyPassword',
						data: {
							UserID: userInfo.UserID,
							oldPassword: that.oldPassword,
							newPassword: that.newPassword
						},
						method:'POST',
						header:{
							'content-type': 'application/x-www-form-urlencoded'
						},
						success: (res) => {
							if(res.data.code)
								App.errorToast(res.data.msg)
							else{
								App.successToast("密码修改成功")
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
</style>
