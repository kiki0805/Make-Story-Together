import React from 'react';
import { connect } from "react-redux";
import { fetchGroupList, fetchGroupDetail } from '../api/groups';
import { Card, Layout, Icon, Button, Affix } from 'antd';
import { STATUS, createGroup, doneCreateGroup } from '../actions/groups';
import WrappedGroupForm from '../components/groupCreationForm';
import '../styles/group.css';
const { Sider, Content, Header } = Layout;

class Group extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            groups: [], // default collapsed
            groupDetail: null,
            collapsed: true
        }
    }

    componentDidMount() {
        this.fetch(this)
    }

    fetch(that, groupID=null) {
        console.log('fetch group list');
        fetchGroupList().then((groups) => {
            that.setState({groups});
        })
        if (groupID != null) {
            fetchGroupDetail(groupID).then((groupDetail) => {
                that.setState({groupDetail});
            });
        }
    }

    onCollapse = collapsed => {
        this.setState({ collapsed });
    };

    handleMore = groupID => {
        fetchGroupDetail(groupID).then((groupDetail) => {
            this.setState({groupDetail});
        });
        this.onCollapse(false);
    }

    toggle = () => {
        this.onCollapse(!this.setState.collapsed);
        this.setState({groupDetail: null});
        this.props.doneCreateGroup();
    }

    handleNewGroup = () => {
        this.onCollapse(false);
        this.setState({groupDetail: null});
        this.props.createGroup();
    }

    render() {  
        return (
            <Layout>
                <Affix offsetTop={0}>
                    {this.props.token === null ? null : 
                        <Header className='groupHeader' style={{ width: '100%' }}>
                            <Button onClick={this.handleNewGroup} size='small'>
                                New Group
                            </Button>
                        </Header>
                    }
                </Affix>
                <Layout 
                    style={this.props.token === null ? null : { marginTop: 40, width: '100%' }}
                >
                    <Content style={{overflow: 'initial'}}>
                        {this.state.groups.map((group) => 
                            <Card 
                                key={group.id}
                                title={group.name} 
                                extra={<Icon onClick={() => this.handleMore(group.id)} type="more" />} 
                                style={{ width: 300 }}
                            >
                                <p>Owner {group.owner}</p>
                                <p>{group.description}</p>
                            </Card>
                            
                        )}
                    </Content>
                    <Sider
                        className='groupSider'
                        trigger={null}
                        collapsible 
                        collapsed={this.state.collapsed} 
                        onCollapse={this.onCollapse} 
                        reverseArrow={true}
                        width="450px"
                        collapsedWidth='0px'
                        style={{
                            overflow: 'auto',
                            position: 'fixed',
                            right: 0,
                            height: '100%'
                        }}
                    >
                        {this.state.collapsed ? null : <Icon onClick={this.toggle} style={{ color: 'rgba(255, 255, 255, 0.7)', fontSize: '40px' }}  type="menu-unfold" />}
                        {this.state.groupDetail === null ? null :
                            <div style={{ color: 'rgba(255, 255, 255, 0.7)' }}>
                                <p>{this.state.groupDetail.name}</p>
                                <p>Owner {this.state.groupDetail.owner}</p>
                                <p>{this.state.groupDetail.description}</p>
                            </div>
                        }
                        {this.props.status === STATUS.CREATING_GROUP ? <WrappedGroupForm callback={this.fetch} that={this} /> : null}
                    </Sider>
                </Layout>
            </Layout>
        )
    }
}


const mapStateToProps = (state) => {
    return {
        token: state.writers.token,
        status: state.groups.status
    }
}

export default connect(mapStateToProps, {createGroup, doneCreateGroup})(Group);

