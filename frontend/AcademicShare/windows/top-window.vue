<template>
	<view class="container">
		<view class="logo">
			<image src="../static/index/logo.png" mode="aspectFit"></image>
			<text>ECNU学术资源共享</text>	
		</view>
		<view class="myTabBar">
			<navigator open-type="reLaunch" url="/pages/index/index">
				首页
			</navigator>
			<navigator open-type="reLaunch" url="/pages/upload/upload">
				上传
			</navigator>
		</view>
		<!--
		<SearchBar style="margin-left:310px;"></SearchBar>
		-->
		<view class="search">
			<input class="text" :disabled="disableInput" :value="searchTitle" :placeholder="inputHint" @input="getTitle" />
			<image v-if="searchTitle.length == 0" src="../static/index/search.png" mode="aspectFit"></image>
		</view>
		
		<view class="myinfo">
			<image src="../static/index/avatar.png" mode="aspectFit"></image>
			<navigator open-type="reLaunch" url="/pages/myinfo/myinfo">{{userInfo.nickName}}</navigator>	
		</view>	
	</view>
</template>

<script>
	export default {
		data() {
			return {
				searchTitle: '',
				userInfo: {
					"nickName" : '登录/注册'
				},
				disableInput: false,
				inputHint: '输入资源名称/内容搜索'
			}
		},			
		mounted() {		
			try{		
				let current_userinfo = uni.getStorageSync('userInfo')			
				if(current_userinfo && current_userinfo != 'empty'){
					this.userInfo = current_userinfo
				}
				
			}catch(e){
				try{
					uni.setStorageSync("userInfo", 'empty')
				}catch(e){
					console.log(e)
				}
			}
			uni.$on('login',(userInfo)=>{
				if(userInfo && userInfo != 'empty')
					this.userInfo = userInfo;  
				else
					this.userInfo = {
						"nickName" : '登录/注册'
					}
			})
			uni.$on('disableInput',(res)=>{
				this.disableInput = res
				if(res){
					this.inputHint = '请在首页搜索'
					this.searchTitle = ''
				}
				else
					this.inputHint = '输入资源名称/内容搜索'
			})
		},
		destroyed:function(){
			uni.$off('login')
			uni.$off('disableInput')
		},
		methods:{
			getTitle:function(e){
				this.searchTitle = e.target.value	
				uni.$emit('getSearchTitle', this.searchTitle)
			},	
		}
		
	}
</script>

<style>
	.container {
		/*border:#000000 solid 2px;*/
		height: 60px;
		padding: 0 15px;
		display: flex;
		flex-direction: row;
		align-items: center;
		box-sizing: border-box;
		border-bottom: #DDDDDD solid 2px;
		background-color: #FFFFFF;
		color: #333;
	}
	.logo {
		width:18%;
		height:60px;
		/*border:#000000 solid 2px;*/
		display: flex;
		flex-direction: row;
		align-items: center;
	}
	.logo image {
		width:20%;
		height:100%;
		/*border:#000000 solid 2px;*/
	}
	.logo text {
		
		height:50px;
		/*border:#000000 solid 2px;*/
		display: flex;
		flex-direction: row;
		align-items: center;
		font-size: small;
		font-weight: bold;
	}
	.myTabBar {
		margin-left: 5px;
		width:7%;
		/*border: #000000 solid 2px;*/
		display: flex;
		flex-direction: row;
		color: #333;
		justify-content: space-between;
	}
	.myTabBar navigator{
		/*border: #000000 solid 2px;*/
	}
	.myinfo{
		position: absolute;
		right: 20px;
		width:17%;
		height:50px;
		/*border:#000000 solid 2px;*/
		display: flex;
		flex-direction: row;
		align-items: center;
	}
	.myinfo image {
		width:20%;
		height:100%;
		/*border:#000000 solid 2px;*/
	}
	.myinfo navigator {
		overflow: auto;
		max-width:80%;
		margin-left: 2px;
		height:100%;
		/*border:#000000 solid 2px;*/
		display: flex;
		flex-direction: row;
		align-items: center;
		font-size: small;
	}	
	.search{
		margin-left: 300px;
		padding: 2px;
		width:300px;
		height: 35px;
		display: flex;
		align-items: center;
		border: #3F536E solid 1px;
		border-radius: 5px 5px 5px 5px;
		justify-content: space-between;
	}
	.search .text{
		overflow: auto;
		height:35px;
		width:260px;
		font-size: small;
		color: #808080;
		/*border:#000000 solid 2px;*/
		display: flex;
		align-items: center;
		color: #000000;
	}
	.search image {
		width:30px;	
		height:25px;
		/*border:#000000 solid 2px;*/
	}
</style>
