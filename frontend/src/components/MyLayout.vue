<template>
  <div>
    <Layout class="self-layout">
      <Sider breakpoint="md" 
            collapsible 
            width='140px'
            :collapsed-width="40" 
            v-model="isCollapsed  "
            v-bind:style="styleObj"
            class="self-sider">
        <Menu 
          theme="light" 
          width="auto" 
          @on-select='handleSelection'
          :class="menuitemClasses"
        >
          <MenuItem name="home"
          >
            <Icon type="ios-home-outline"></Icon>
            <span>home</span>
          </MenuItem>
          <MenuItem 
            name="category">
            <Icon type="ios-apps-outline"></Icon>
            <span>category</span>
          </MenuItem>
          <MenuItem name="tag">
            <Icon type="ios-pricetags-outline"></Icon>
            <span>tag</span>
          </MenuItem>
          <MenuItem name="about">
            <Icon type="ios-person"></Icon>
            <span>about</span>
          </MenuItem>
          <MenuItem name="profile">
            <Icon type="ios-person-outline"></Icon>
            <span>profile</span>
          </MenuItem>
          <div v-show="loginUser" v-bind="getLoginUser">
            <!-- 根据用户是否登入显示login 还是logout -->            
            <MenuItem name="compose">
              <Icon type="ios-create-outline"></Icon>
              <span>compose</span>
            </MenuItem>
            <MenuItem name="logout">
              <Icon type="ios-exit-outline"></Icon>
              <span>logout</span>
            </MenuItem>
          </div>
          <MenuItem 
            name="login" 
            v-show="!loginUser"
          >
            <Icon type="ios-log-in"></Icon>
            <span>login</span>
          </MenuItem>
        </Menu>
        <div slot="trigger"></div>
      </Sider>
      <Content :style="contentObj" class="content">
        <router-view></router-view>
      </Content>
    </Layout>
  </div>
</template>

<script>
import * as types from '../store/mutationTypes'

export default {
  name: 'myLayout',
  data: function() {	
    return {
      loginUser: '',
      isCollapsed: false
    }
  },
  methods: {
    handleSelection (name) {
      if (name === 'logout') {
        // this.$router.push('/' + name)
        this.$axios.get('/logout')
          .then(
          )
          .catch(

          )
        this.$store.commit(types.LOGOUT)
        this.$router.push('/')
      } else {
        // 这个要针对根目录
        this.$router.push('/' + name)
      }
    }
  },
  computed: {
    getLoginUser () {
      this.loginUser = this.$store.state.loginUser
      return null
    },
    menuitemClasses: function () {
      return [
        'menu-item',
        this.isCollapsed ? 'collapsed-menu' : ''
      ]
    },
    styleObj () {
      let screenWidth =  window.screen.width
      let marginLeftWidth = '12em'
      // 因为iview默认的就是480作为触发
      if (screenWidth < 480){
        marginLeftWidth = '0'
      }
      return {
        marginLeft: this.isCollapsed ? '0' : marginLeftWidth
      }
    },
    contentObj () {
      let screenWidth =  window.screen.width
      let marginRightWidth = '18em'
      // 因为iview默认的就是480作为触发
      if (screenWidth < 480){
        marginRightWidth = '0'
      }
      return {
        marginRight: this.isCollapsed ? '0' : marginRightWidth
      }
    }
  }
}
</script>

<style scoped>

.self-layout {
  background-color: #fff;
}

.self-sider {
  background-color: #fff;
  margin-top: 5em;
}

.content {
  background-color: #fff;
  padding: 0em 2em;
  font-size: 16px;
  min-width: 340px;
}

.menu-item span{
    display: inline-block;
    overflow: hidden;
    width: 69px;
    text-overflow: ellipsis;
    white-space: nowrap;
    vertical-align: bottom;
    transition: width .2s ease .2s;
}
.menu-item i{
    transform: translateX(0px);
    transition: font-size .2s ease, transform .2s ease;
    vertical-align: middle;
    font-size: 16px;
}
.collapsed-menu span{
    width: 0px;
    transition: width .2s ease;
}
.collapsed-menu i{
    transform: translateX(5px);
    transition: font-size .2s ease .2s, transform .2s ease .2s;
    vertical-align: middle;
    font-size: 22px;
}

</style>