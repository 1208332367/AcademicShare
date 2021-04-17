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
				<view class="title">用户登录</view>
			<!-- #endif--> 
			<view class="body">	
				<input class="text" placeholder="账号/学号" maxlength="16" @input="getAccount"/>
				<input class="text" type="password" placeholder="密码" maxlength="16" @input="getPassword"/>
				<button class="submit" @click="submit">
					登录
				</button>
				<view class="extra">
					<view class="left">
						<view @click="register">注册</view>
						<view>
							<uni-link :href="adminUrl" style="margin-left: 10rpx;font-size: small;color: #444444;text-decoration: none;" text="管理员登录"></uni-link>
						</view>
					</view>
					<view class="right" @click="forget">
						忘记密码？
					</view>
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
				account: '',
				password: '',
				islegalAccount: false,
				islegalPassword: false,
				adminUrl: ''
			}
		},	
		onLoad() {
			this.app_platform = App.globalData.app_platform
			this.adminUrl = App.globalData.domain + 'admin'
			uni.$emit('disableInput', true)
		},		
		onShow() {
			
		},	
		methods: {
			register:function(e){
				uni.navigateTo({
					url: "../register/register"
				})
			},
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
			submit:function(){
				if(!this.account.length){
					App.errorToast('账号不能为空')
					return
				}
				if(!this.password.length){
					App.errorToast('密码不能为空')
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
				if(this.password.length < 8 || this.password.length > 16){
					App.errorToast('密码必须为8-16位')
					return
				}
				if(!this.islegalPassword){
					App.errorToast('密码只能为数字、字母')
					return
				}			
				var that = this
				uni.request({
					url: App.globalData.rootUrl + 'user/login',
					data: {
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
							App.successToast("登录成功")
							setTimeout(function(){
								uni.switchTab({
									url: '/pages/myinfo/myinfo',
								})
							}, 500)
						}
					},
					fail: (res) => {
						App.requestFailToast()
					}
				})
			},			
			forget:function(){
				uni.showModal({
					showCancel: false,
					title: '请联系管理员 王佳镐\nQQ: 1208332367'
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
		height: 40px;
		font-size: small;
		display: flex;
		align-items: center;
		justify-content: space-between;
		/*border: #000000 solid 2rpx;*/
		color: #444444;
	}
	.body .extra .left{
		width: 50%;
		/*border: #000000 solid 2rpx;*/
		display: flex;
	}
	.body .extra .right{
		width: 40%;
		/*border: #000000 solid 2rpx;*/
		display: flex;
		justify-content: flex-end;
	}
</style>
