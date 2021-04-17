<template>
	<view>
		<view class="page">
			<view class="main">
				<view v-if="app_platform!='PC'" style="width: 100%;">
					<AppHeader></AppHeader>
				</view>
				
				<view class="choice">
					<view class="item" style="margin-top: 5px;">
						<view class="title">学科大类</view>
						<view class="bg-gray py-2 px-1" style="width: 80%;" >
							<Row cols="5" gutter="3" >
								<block v-for="(profession, index) in professions" :key="index">
									<o-col v-if="!profession.isChoose"  @Click="professionReverse(index)" >{{profession.name}}</o-col>
									<o-col v-if="profession.isChoose" v-bind:isChoose="true" @Click="professionReverse(index)">{{profession.name}}</o-col>
								</block>
							</Row>		
						</view>
					</view>
					<view class="item">
						<view class="title">访问限制</view>
						<view class="bg-gray py-2 px-1" style="width: 80%;">
							<Row cols="5" gutter="3" >
								<block v-for="(visit, index) in visits" :key="index">
									<o-col v-if="!visit.isChoose"  @Click="visitReverse(index)">{{visit.content}}</o-col>
									<o-col v-if="visit.isChoose" v-bind:isChoose="true" @Click="visitReverse(index)">{{visit.content}}</o-col>
								</block>
							</Row>
						</view>
					</view>
					<view class="item">
						<view class="title">排序规则</view>
						<view class="bg-gray py-2 px-1" style="width: 80%;">
							<Row v-if="app_platform!='PC'" cols="4" gutter="3" >
								<block v-for="(order, index) in orders" :key="index">
									<o-col v-if="!order.isChoose" v-bind:isChoose="false" @Click="orderReverse(index)">{{order.content}}</o-col>
									<o-col v-if="order.isChoose" v-bind:isChoose="true" @Click="orderReverse(index)">{{order.content}}</o-col>
								</block>
							</Row>
							<Row v-else cols="5" gutter="3" >
								<block v-for="(order, index) in orders" :key="index">
									<o-col v-if="!order.isChoose" v-bind:isChoose="false" @Click="orderReverse(index)">{{order.content}}</o-col>
									<o-col v-if="order.isChoose" v-bind:isChoose="true" @Click="orderReverse(index)">{{order.content}}</o-col>
								</block>
							</Row>
						</view>
					</view>
				</view>
				
				<view class="resource_list">
					<block v-if="resourceListLength > 0">
						<block v-for="(resource, index) in resourceList" :key="index">
							<Resource :item="resource" v-if="index == 0" style="margin-top: 15px;border-bottom: #D3D3D3 solid 2px;"></Resource>
							<Resource :item="resource" v-if="index > 0 && index < 3" style="border-bottom: #D3D3D3 solid 2px;"></Resource>
							<Resource :item="resource" v-if="index == 3" ></Resource>
						</block>
					</block>
					<block v-else>
						<view class="no_resource">暂无相关资源</view>
					</block>
					
				</view>
				
				<view class="page_select">
					<view class="left">
						<view class="item" @click="goToFirstPage">首页</view>
						<view class="item" @click="goToPrePage">上一页</view>
						<view class="item" @click="goToNextPage">下一页</view>
						<view class="item" @click="goToLastPage">尾页</view>
					</view>
					<view class="right">
						<view class="item">页码：{{pageIndex}}/{{totalPage}}</view>
						<input class="navigate" maxlength="6" @input="getPageJmpIndex" :value="pageJmpIndex"/>
						<view class="item" @click="jumpToInputPageIndex">跳转</view>
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
				professions: [],
				visits:[
					{"content": "无限制", "isChoose": true },
					{"content": "仅校内", "isChoose": false },
				],
				orders:[
					{"content": "最近更新", "isChoose": true },
					{"content": "最高评分", "isChoose": false },
					{"content": "最多下载", "isChoose": false },
				],
				ProfessionIDs: [],
				visitCtrl: 1,
				orderRule: 0,
				pageIndex: 1,
				totalPage: 1,
				pageJmpIndex: '',
				islegalPageJmpIndex: false,
				searchTitle: '',
				resourceList: [],
				resourceListLength: 0,
				userInfo: null,
			}
		},	
		onLoad() {
			this.app_platform = App.globalData.app_platform
			this.getProfession()	
		},	
		onShow() {
			uni.$emit('disableInput', false)
			uni.$on('getSearchTitle',(searchTitle)=>{
				this.searchTitle = searchTitle
				this.getResourceList()
			})
			this.getResourceList()			
		},	
		onPullDownRefresh() {
			this.getResourceList()
		},		
		destroyed(){
			uni.$off('getSearchTitle')
		},	
		methods: {
			getPageJmpIndex:function(e){
				this.pageJmpIndex = e.target.value
				if(!e.target.value.length)
					return
				var re = /^[0-9]+$/gi;
				if(!re.test(e.target.value)){
					App.errorToast('页码只能为整数')
					this.islegalPageJmpIndex = false
					return
				}
				this.islegalPageJmpIndex = true	
			},
			jumpToInputPageIndex:function(){
				if(!this.pageJmpIndex.length){
					App.errorToast('请输入页码')
					return
				}
				if(!this.islegalPageJmpIndex){
					App.errorToast('页码只能为整数')
					return
				}	
				var currentIndex = parseInt(this.pageJmpIndex)
				if(currentIndex < 1 || currentIndex > this.totalPage){
					App.errorToast('页码超出范围')
					return
				}
				this.pageIndex = this.pageJmpIndex
				this.getResourceList()
			},
			goToFirstPage:function(){
				this.pageIndex = 1
				this.getResourceList()
			},
			goToLastPage:function(){
				this.pageIndex = this.totalPage
				this.getResourceList()
			},
			goToPrePage:function(){
				if(this.pageIndex > 1)
					this.pageIndex --
				this.getResourceList()
			},
			goToNextPage:function(){
				if(this.pageIndex < this.totalPage)
					this.pageIndex ++
				this.getResourceList()
			},
			getProfession:function(){
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
							arr.unshift({
								'id': 0,
								'name': '不限',
								'isChoose': true
							})
							for(var i = 1; i < arr.length; i++)
								arr[i]['isChoose'] = false
							that.professions = arr
							//console.log(that.professions)
						}
					},
					fail: (res) => {
						App.requestFailToast()
					}
				})
			},
			professionReverse:function(index){
				if(index == 0){
					this.professions[0].isChoose = true;
					for(var i = 1; i < this.professions.length; i++){
						this.professions[i].isChoose = false
					}
				}
				else{
					this.professions[0].isChoose = true;
					this.professions[index].isChoose = !this.professions[index].isChoose;
					for(var i = 1; i < this.professions.length; i++){
						if(this.professions[i].isChoose){
							this.professions[0].isChoose = false;
							break;
						}	
					}
				}
				this.getResourceList()		
			},
			visitReverse:function(index){
				if(index == 0){
					this.visits[0].isChoose = true;
					this.visits[1].isChoose = false;
				}
				else{
					this.visits[0].isChoose = true;
					this.visits[1].isChoose = !this.visits[1].isChoose;
					if(this.visits[1].isChoose)
						this.visits[0].isChoose = false;	
				}
				this.getResourceList()
			},
			orderReverse:function(index){
				if(index == 0){
					this.orders[0].isChoose = true;
					for(var i = 1; i < 3; i++){
						this.orders[i].isChoose = false
					}
				}
				else{
					this.orders[0].isChoose = true;
					for(var i = 1; i < 3; i++){
						if(i == index)
							this.orders[i].isChoose = !this.orders[i].isChoose
						else
							this.orders[i].isChoose = false
					}
					for(var i = 1; i < 3; i++){
						if(this.orders[i].isChoose){
							this.orders[0].isChoose = false;
							break;
						}	
					}
				}
				this.getResourceList()
			},
			getSelection:function(){
				this.ProfessionIDs = []
				for(var i = 0; i < this.professions.length; i++){
					if(this.professions[i].isChoose){
						//console.log(i)
						this.ProfessionIDs.push(this.professions[i].id)
					}	
				}
				for(var i = 0; i < this.visits.length; i++){
					if(this.visits[i].isChoose){
						this.visitCtrl = i ^ 1
					}	
				}
				for(var i = 0; i < this.orders.length; i++){
					if(this.orders[i].isChoose){
						this.orderRule = i
					}	
				}
			},
			getResourceList:function(){
				this.getSelection()
				var that = this
				uni.showLoading({
					title: '加载中...'
				})
				uni.request({
					url: App.globalData.rootUrl + 'resource/getSelectedResource',
					data: {
						visitCtrl: that.visitCtrl,
						orderRule: that.orderRule,
						pageIndex: that.pageIndex,
						searchTitle: that.searchTitle,
						ProfessionIDs: JSON.stringify(that.ProfessionIDs)
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
							that.totalPage = res.data.data.totalPages
							that.pageIndex = res.data.data.pageNum
							var arr = res.data.data.resourceList
							for(var i = 0; i < res.data.data.length; i++){
								arr[i].ctime = App.getDateFromCtime(arr[i].ctime)
								arr[i].avgScore = App.getFixedScore(arr[i].avgScore)
							}
							that.resourceList = arr
							that.pageJmpIndex = ''
							//console.log(res.data)
						}
					},
					fail: (res) => {
						uni.hideLoading()
						uni.stopPullDownRefresh()
						App.requestFailToast()
					}
				})
			},
		}
	}
</script>

<style>
	.choice{
		background-color: white;
		position: fixed;
		z-index: 9999;
		font-size: 90%;
		width: 100%;
		height:170px;
		/*border: #000000 solid 2px;*/
		padding-bottom:15px;
		/*border-bottom:#A1DCC1 solid 2px;*/
		border-bottom:#666666 solid 2px;	
		display: flex;
		flex-direction: column;
		padding-left:25rpx;
	}
	/* #ifdef MP-WEIXIN */
	.choice{
		height: 140px;
	}
	/* #endif */
	.choice .item{
		width: 100%;
		display: flex;
		margin-top: 10px;
	}
	.choice .item .title{
		width: 20%;
		font-weight: bold;
		padding-top: 5px;
		margin-left: 5rpx;
	}
	@media only screen and (min-width: 1029px){
		.choice{
			width:48%;
		}
		.choice .item .title{
			width: 80px;
			font-weight: bold;
		}
	}
	.resource_list{
		width: 97%;
		height: 95%;
		overflow-y: auto;
		border-bottom:#666666 solid 2px;
		margin-top:230px;
		/*border: #000000 solid 2px;*/
	}
	.page_select{
		/*border: #000000 solid 2px;*/
		width: 100%;
		height: 80px;
		display: flex;
		font-size: 90%;
	}
	@media only screen and (min-width: 1029px){
		.resource_list{
			margin-top:165px;
			height: 1200px;
		}
		.page_select{
			font-size: 110%;
		}
	}
	.resource_list .no_resource{
		height: 100%;
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 110%;
		font-weight: bold;
	}
	@media only screen and (max-width: 1028px){
		.choice{
			margin-top:61px;	
		}
	}
	.page_select .left{
		width: 52%;
		height: 100%;
		/*border: #000000 solid 1px;*/
		display: flex;
		align-items: center;
		justify-content: flex-end;
		padding-right: 10px;
	}
	.page_select .right{
		width: 48%;
		height: 100%;
		/*border: #000000 solid 1px;*/
		display: flex;
		align-items: center;
		padding-left: 5px;
	}
	.page_select .right .navigate{
		width: 40px;
		margin-left: 10px;
		height: 10px;
		background-color: white;
		border: #000000 solid 1px;
	}
	@media only screen and (min-width: 1029px){
		.page_select .left .item{
			margin-right: 10px;
			/*border: #000000 solid 1px;*/
		}
		.page_select .right .item{
			margin-left: 5px;
			/*border: #000000 solid 1px;*/
		}
	}
	@media only screen and (max-width: 1028px){
		.page_select .left .item{
			margin-right: 10rpx;
			/*border: #000000 solid 1px;*/
		}
		.page_select .right .item{
			margin-left: 5rpx;
			/*border: #000000 solid 1px;*/
		}
		.page_select .right .navigate{
			margin-left: 10rpx;
			width: 50rpx;
		}
	}
</style>
