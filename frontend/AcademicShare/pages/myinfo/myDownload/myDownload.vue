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
					<view class="title">我的下载</view>
				<!-- #endif--> 
				<view class="body">	
					<block v-if="resourceListLength > 0">
						<view class="resource_list">
							<block v-for="(resource, index) in resourceList" :key="index">
								<block v-if="index < 4">
									<Resource :item="resource" style="border-bottom: #D3D3D3 solid 2px;"></Resource>
								</block>
								<block v-else>
									<Resource :item="resource" v-if="index < resourceListLength - 1" style="border-bottom: #D3D3D3 solid 2px;"></Resource>
									<Resource :item="resource" v-if="index == resourceListLength - 1"></Resource>
								</block>
							</block>
						</view>
					</block>
					<block v-else>
						<view class="no_resource">暂无相关资源</view>
					</block>	
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
				resourceList: [],
				resourceListLength: 0,	
			}
		},	
		onLoad() {
			this.app_platform = getApp().globalData.app_platform
			uni.$emit('disableInput', true)
		},	
		onShow() {
			App.checkLoginStatus()
			this.getResourceList()
		},	
		onPullDownRefresh() {
			this.getResourceList()
		},		
		methods: {
			getResourceList:function(){
				var that = this
				try{
					var userInfo = uni.getStorageSync('userInfo')
					uni.showLoading({
						title: '加载中...'
					})
					uni.request({
						url: App.globalData.rootUrl + 'user/getDownloadResource',
						data: {
							UserID: userInfo.UserID
						},
						method:'POST',
						header:{
							'content-type': 'application/x-www-form-urlencoded'
						},
						success: (res) => {
							uni.hideLoading()
							uni.stopPullDownRefresh()
							if(res.data.code)
								App.errorToast(res.data.msg)
							else{
								that.resourceListLength = res.data.data.length
								var arr = res.data.data.resourceList
								for(var i = 0; i < res.data.data.length; i++){
									arr[i].ctime = App.getDateFromCtime(arr[i].ctime)
									arr[i].avgScore = App.getFixedScore(arr[i].avgScore)
								}
								that.resourceList = arr
							}
						},
						fail: (res) => {
							uni.hideLoading()
							uni.stopPullDownRefresh()
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
		width: 100%;
		margin-top:20px;
		height:70%;
		/*border: #000000 solid 2rpx;*/
		display: flex;
		flex-direction: column;
		align-items: center;
		border-top:#666666 solid 2px;
		border-bottom:#666666 solid 2px;
	}
	.resource_list{
		width: 95%;
		/*height: 100%;*/
		overflow-y: auto;
	
		/*border: #000000 solid 2px;*/
	}
	@media only screen and (min-width: 1029px){
		.body{
			margin-top:30px;
		}
		.resource_list{
			width: 98%;
			width: 95%;
		}
	}
	.no_resource{
		height: 100%;
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 110%;
		font-weight: bold;
	}
</style>
