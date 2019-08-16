import React from 'react';
import SiderLayout from './containers/sider';
import Profile from './containers/profile';
import Explore from './containers/explore';
import GroupList from './components/groupList';
import GroupDetail from './components/groupDetail';
import Story from './containers/story';
import PageNotFound from './containers/notfound'
import HeaderLayout from './containers/header';
import { BrowserRouter as Router, Route, Switch, Redirect } from "react-router-dom";
import { Layout, BackTop } from 'antd';
import ScrollToTop from './containers/scrollToTop';
import './styles/layout.css';
import 'antd/dist/antd.css';
const { Content } = Layout;

class App extends React.Component {
  render() {
    return (
      <Layout style={{ minHeight: '100vh' }}>
        <Router>
          <ScrollToTop>
            <SiderLayout />
            <Layout>
              <HeaderLayout />
              <Content style={{ marginTop: '40px'}}>
                <Switch>
                  <Route exact path="/">
                    <Redirect to="/explore" />
                  </Route>
                  <Route path="/profile" component={Profile} />
                  <Route path="/explore" component={Explore} />
                  <Route exact path="/group" component={GroupList} />
                  <Route exact path='/group/:groupID' component={GroupDetail} />
                  <Route path="/story" component={Story} />
                  <Route component={PageNotFound} />
                </Switch>
              </Content>
            </Layout>
          </ScrollToTop>
        </Router>
        <BackTop />
      </Layout>
    );
  }
}

export default App;
