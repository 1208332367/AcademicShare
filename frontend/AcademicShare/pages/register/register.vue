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
					<view class="title">用户注册</view>
				<!-- #endif--> 
				<view class="body">	
					<input class="text" placeholder="账号,8-16位数字" maxlength="16" @input="getAccount" />
					<input class="text" placeholder="昵称,10字以内汉字、字母" maxlength="10" @input="getNickName" />
					<input class="text" type="password" placeholder="密码,8-16位数字、字母" maxlength="16" @input="getPassword" />
					<input class="text" type="password" placeholder="再次输入密码" maxlength="16" @input="getConfirmPassword" />
					<button class="submit" @click="submit">
						注册
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
				account: '',
				nickName: '',
				password: '',
				confirmPassword: '',
				islegalAccount: false,
				islegalNickName: false,
				islegalPassword: false,
				islegalConfirmPassword: false,		
			}
		},		
		onLoad() {
			this.app_platform = App.globalData.app_platform
			uni.$emit('disableInput', true)
		},	
		onShow() {
			
		},		
		methods: {
			getAccount:function(e){
				this.account = e.target.value
				if(!e.target.value.length)
					return
				var re = /^[0-9]+$/gi;
				if(!re.test(e.target.value)){
					App.errorToast('请输入数字')
					this.islegalAccount = false
					return
				}
				this.islegalAccount = true			
			},
			getNickName:function(e){
				this.nickName = e.target.value
				if(!e.target.value.length)
					return
				var re = /^[\u4e00-\u9fa5a-z]+$/gi;
				if(!re.test(e.target.value)){
					App.errorToast('请输入汉字或字母')
					this.islegalNickName = false
					return
				}
				this.islegalNickName = true
			},
			getPassword:function(e){
				this.password = e.target.value
				if(!e.target.value.length)
					return
				var re = /^[0-9,a-z]+$/gi;
				if(!re.test(e.target.value)){
					App.errorToast('请输入数字或字母')
					this.islegalPassword = false
					return
				}			
				this.islegalPassword = true
			},
			getConfirmPassword:function(e){
				this.confirmPassword = e.target.value
				if(!e.target.value.length)
					return
				var re = /^[0-9,a-z]+$/gi;
				if(!re.test(e.target.value)){
					App.errorToast('请输入数字或字母')
					this.islegalConfirmPassword = false
					return
				}		
				this.islegalConfirmPassword = true
			},
			submit:function(){
				if(!this.account.length){
					App.errorToast('账号不能为空')
					return
				}
				if(!this.nickName.length){
					App.errorToast('昵称不能为空')
					return
				}
				if(!this.password.length){
					App.errorToast('密码不能为空')
					return
				}
				if(!this.confirmPassword.length){
					App.errorToast('确认密码不能为空')
					return
				}
				if(this.account.length < 8 || this.account.length > 16){
					App.errorToast('账号必须为8-16位')
					return
				}
				if(!this.islegalAccount){
					App.errorToast('账号只能包含数字')
					return
				}
				if(this.nickName.length > 10){
					App.errorToast('昵称必须在10字以内')
					return
				}
				if(!this.islegalNickName){
					App.errorToast('昵称只能为汉字、字母')
					return
				}
				if(this.password.length < 8 || this.password.length > 16){
					App.errorToast('密码必须为8-16位')
					return
				}
				if(!this.islegalPassword){
					App.errorToast('密码只能为数字、字母')
					return
				}
				if(this.password != this.confirmPassword){
					App.errorToast('两次输入的密码不一致')
					return
				}
				var that = this
				uni.request({
					url: App.globalData.rootUrl + 'user/register',
					data: {
						nickName: that.nickName,
						account: that.account,
						password: that.password
					},
					method:'POST',
					header:{
						'content-type': 'application/x-www-form-urlencoded'
					},
					success: (res) => {
						if(res.data.code)
							App.errorToast(res.data.msg)
						else{
							var info = res.data.data
							try{
								info['cachetimestamp'] = App.getCurrentSecond()
								uni.setStorageSync("userInfo", info)
							}
							catch(e){
								App.errorToast("用户信息缓存失败")
							}
							//console.log(res.data.data)
							uni.$emit('login', info)
							App.successToast("注册成功")
							setTimeout(function(){
							  /*uni.navigateBack({
							  	delta: 2
							  })*/
							  uni.switchTab({
							  	  url: '/pages/myinfo/myinfo'
							  })
							}, 500)
							//console.log(App.globalData.userInfo)
						}
					},
					fail: (res) => {
						App.requestFailToast()
					}
				})
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
		height:350px;
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
