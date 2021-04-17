<template>
	<view>
		<view class="page">
			<view class="main">
				<!--
				<view v-if="app_platform!='PC'" style="width: 100%;">
					<AppHeader></AppHeader>
				</view>
				-->
				<Resource class="detail" v-bind:isDetail="true" :item="resourceInfo"></Resource>	
				<view class="comment_list">
					<block v-if="resourceInfo.commentCount > 0">
						<block v-for="(comment, index) in resourceInfo.commentList" :key="index">
							<CommentCard :commentInfo="comment" ></CommentCard>
						</block>
					</block>
					<block v-else>
						<view class="no_comment">暂无相关评论</view>
					</block>
					
				</view>
				<view class="make_comment">
					<view class="stars">
						<view v-for="(num ,index) in 5" :key="index" @click="chooseStar(index)">	
							<image :src="startCount>=index?fullStarImg:emptyStarImg" mode="aspectFit" ></image>
						</view>	
					</view>
					
					<view class="inputText">
						<input class="text" :value="inputComment" placeholder="写下你的评论(25字以内)..." maxlength="25" @input="getInputComment"/>
						<view class="submit" @click="submitComment">
							评论
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
	import fullStar from "../../static/component/comment/full_star.png"
	import emptyStar from "../../static/component/comment/empty_star.png"
	let App = getApp()
	export default {
		data() {
			return {
				app_platform: 'PC',
				ResourceID: 0,
				resourceInfo: {},
				inputComment: '',
				chooseScore: 2,	
				startCount: 0,
				fullStarImg: fullStar,
				emptyStarImg: emptyStar,
				UserID: 0,
			}
		},		
		onLoad(option) {
			this.app_platform = App.globalData.app_platform
			this.ResourceID = option.ResourceID
			this.UserID = option.UserID
			uni.$emit('disableInput', true)
			//console.log(this.ResourceID)
		},		
		onShow() {
			this.getResourceInfo()
			uni.$on('deleteComment',()=>{
				this.getResourceInfo()
			})
		},		
		onPullDownRefresh() {
			this.getResourceInfo()
		},	
		methods: {
			getResourceInfo:function(){
				var that = this
				uni.showLoading({
					title: '加载中...'
				})
				uni.request({
					url: App.globalData.rootUrl + 'resource/getResouceDetailByID',
					data: {
						ResourceID: that.ResourceID,
					},
					method:'POST',
					header:{
						'content-type': 'application/x-www-form-urlencoded'
					},
					success: (res) => {
						uni.hideLoading()
						uni.stopPullDownRefresh()
						if(res.data.code || !res.data.data.length)
							App.errorToast(res.data.msg)
						else{
							var info = res.data.data
							info.ctime = App.getDateFromCtime(info.ctime)
							info.avgScore = App.getFixedScore(info.avgScore)	
							info.fileSize = App.getFixedFileSize(info.fileSize)
							for(var i = 0; i < info.commentCount; i++){
								info.commentList[i].ctime = App.getDateFromCtime(info.commentList[i].ctime)
								
								if(info.commentList[i].UserID == that.UserID){
									info.commentList[i]['canDelete'] = true
								}
								else{
									info.commentList[i]['canDelete'] = false
								}
							}
							that.resourceInfo = info				
						}
					},
					fail: (res) => {
						uni.hideLoading()
						uni.stopPullDownRefresh()
						App.requestFailToast()
					}
				})
			},
			chooseStar:function(index){
				this.startCount = index
				this.chooseScore = 2 * (parseInt(index) + 1)
			},
			getInputComment:function(e){
				this.inputComment= e.target.value
			},
			submitComment:function(){
				if(!this.inputComment.length){
					App.errorToast('内容不能为空')
					return
				}
				var that = this
				try{
					let current_userinfo = uni.getStorageSync('userInfo')
					uni.showModal({
						showCancel: true,
						title: '确定提交评论？',
						success: (res) =>  {
							if(res.confirm){
								uni.request({
									url: getApp().globalData.rootUrl + 'resource/makeComment',
									data: {
										ResourceID: that.ResourceID,
										UserID: current_userinfo.UserID,
										content: that.inputComment,
										score: that.chooseScore
									},			
									method:'POST',
									header:{
										'content-type': 'application/x-www-form-urlencoded'
									},
									success: (res) => {
										if(res.data.code)
											getApp().errorToast(res.data.msg)
										else{
											getApp().successToast("评论成功")
											that.chooseScore = 2
											that.startCount = 0
											that.inputComment = ''
											that.getResourceInfo()
										}
									},
									fail: (res) => {
										getApp().requestFailToast()
									}
								})
							}
						}
					})			
				}catch(e){
					
				}	
			},
		}
	}
</script>

<style>
	.detail{
		width:95%;
		border-bottom:#888888 solid 2px; 
	}
	@media only screen and (max-width: 1028px){
		.detail{
			/*margin-top: 60px;*/
		}
	}
	.comment_list{
		width: 95%;
		max-height:40%;
		overflow-y: auto;
		margin-top:15px;
		border-bottom:#888888 solid 2px;
	}
	.comment_list .no_comment{
		height: 40px;
		width: 100%;
		display: flex;
		align-items: flex-start;
		justify-content: center;
		font-size: 100%;
		font-weight: bold;
		color: #101010;
	}
	.make_comment{
		width: 95%;
		height:90px;
		/*border-bottom: #D3D3D3 solid 2rpx;*/
		margin-top:20px;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		padding-bottom: 10px;
		/*border: #000000 solid 2rpx;*/
	}
	.make_comment .stars{
		height: 45%;
		display: flex;
		/*border: #000000 solid 2rpx;*/
		align-items: center;
	}
	.make_comment .stars view{
		height: 100%;
	}
	.make_comment .stars image{
		width: 50rpx;
		height: 100%;
		/*border: #000000 solid 2rpx;*/
	}
	.make_comment .inputText{
		width: 100%;
		height: 45%;
		display: flex;
		align-items: center;
		justify-content: space-between;
		/*border: #000000 solid 2rpx;*/
	}
	.make_comment .inputText .text{
		/*overflow: auto;*/
		width:85%;
		height: 100%;
		font-size: small;
		/*border:#000000 solid 2px;*/
		border: #3F536E solid 2rpx;
		display: flex;
		align-items: center;
		color: #000000;
		border-radius: 10rpx 10rpx 10rpx 10rpx;
		padding-left:10rpx;
	}
	.make_comment .inputText .submit{
		width:12%;
		height: 100%;
		border: #ff0000 solid 2rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		color: white;
		background-color: #ff0000;
		border-radius: 10rpx 10rpx 10rpx 10rpx;
	}
</style>
