
import React from 'react';
import { Affix, Layout, Menu, Icon } from 'antd';
import { Link, withRouter } from 'react-router-dom';
import Texty from 'rc-texty';
const { Sider } = Layout;
// const { SubMenu } = Menu;

class SiderLayout extends React.Component {
    constructor() {
      super();
      let currentKey;
      
      switch (window.location.pathname.split('/')[1]) {
        case 'group':
          currentKey = '3';
          break;
        case 'story':
          currentKey = '2';
          break;
        case 'profile':
          currentKey = '9';
          break;
        default:
          currentKey = '1';
          break;
      }

      this.state = {
        collapsed: false,
        currentKey
      };
    }

    // componentDidUpdate() {
    //   console.log(this.props.location.pathname)
    // }

    onCollapse = collapsed => {
      this.setState({ collapsed });
    };
  
    render() {
      return (
        <Affix offsetTop={0}>
          <Sider 
            collapsible 
            collapsed={this.state.collapsed}
            trigger={null}
            style={{
              position: 'fixed',
              height: '100%'
            }}
          ></Sider>
          <Sider 
            collapsible 
            collapsed={this.state.collapsed} 
            onCollapse={this.onCollapse}
            style={{ overflow: 'auto' }}
          >
            {!this.state.collapsed ? 
            (<div className="logo"><Texty>Make Story Together</Texty></div>) :
            (<div className="logo"><Icon type="smile" /></div>)
            }
            
            <Menu 
              theme="dark" 
              defaultSelectedKeys={['explore']}
              selectedKeys={[this.props.location.pathname.split('/')[1]]}
            >
              <Menu.Item key="explore">
                <Link to='/explore'>
                  <Icon type="ellipsis" />
                  <span>Explore</span>
                </Link>
              </Menu.Item>
              <Menu.Item key="profile">
                <Link to='/profile'>
                  <Icon type="idcard" />
                  <span>Account</span>
                </Link>
              </Menu.Item>
              <Menu.Item key="story">
                <Link to='/story'>
                  <Icon type="profile" />
                  <span>Story</span>
                </Link>
              </Menu.Item>
              <Menu.Item key="group">
                <Link to='/group'>
                  <Icon type="team" />
                  <span>Group</span>
                </Link>
              </Menu.Item>
              {/* <SubMenu
                key="sub1"
                title={
                  <span>
                    <Icon type="user" />
                    <span>Groups</span>
                  </span>
                }
              >
                <Menu.Item key="3">Tom</Menu.Item>
                <Menu.Item key="4">Bill</Menu.Item>
                <Menu.Item key="5">Alex</Menu.Item>
              </SubMenu> */}
            </Menu>
          </Sider>
        </Affix>
      );
    }
  }

export default withRouter(SiderLayout);
