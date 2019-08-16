import React from 'react';
import { connect } from 'react-redux';
import { Form, Input, Button, Divider, Select, Popover, Icon } from 'antd';
import '../styles/disciplineForm.css';

const { Option } = Select;


class NakedManage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            groupId: this.props.match.params.groupID,
            groupDetail: this.props.groupDetail,
            selected: [],
            newItem: false
        }
    }

    handleSubmit = e => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (err) {
                return
            }
            console.log(values)
            // createItem(this.props.token, {
            //     creator: this.props.screen_name,
            //     ...values
            // }, 'story').then((res) => {
            //     if (!res.success) {
            //         console.log('create story fail')
            //     }
            //     this.props.doneCreateStory();
            //     this.props.callback(this.props.that, res.id);
            // })
        
        });
    };

    handleChange = (value) => {
        this.setState({
            selected: value
        })
    }

    handleRemove = () => {
        
    }

    handleRemoveDiscipline = (e) => {
        console.log(e.target.id)
    }

    handleAddDiscipline = () => {
        this.toggle();
    }

    toggle = () => {
        this.setState({newItem: !this.state.newItem})
    }

    getOptions = (rule) => {
        let options = [];
        for (let i = 0; i < rule.length; i++) {
            let discipline = rule[i];
            options.push(
                <Button key={discipline.id} id={discipline.id} onClick={this.handleRemoveDiscipline}>
                    <Popover content={this.getContent(discipline)}>
                        {discipline.id}: (registration time required: {discipline.registration_time})-(update cycle required: {discipline.update_cycle})
                    </Popover>
                </Button>
            );
        }
        return options;
    }

    getContent = (discipline) => {
        return (
            <div>
                <strong>Blacklist</strong>
                {discipline.blacklist.map((user) => 
                    <div key={user}>{user}</div>
                )}
                <Divider />
                <strong>Whitelist</strong>
                {discipline.whitelist.map((user) => 
                    <div key={user}>{user}</div>
                )}
            </div>
        )
    }

    render() {
        const { getFieldDecorator } = this.props.form;
        return (
            <div>
                <Form onSubmit={this.handleSubmit}>
                    <Form.Item label='Group Name'>
                        {getFieldDecorator('name')(
                            <Input placeholder={this.state.groupDetail.name} />)}
                    </Form.Item>
                    <Form.Item label='Description'>
                        {getFieldDecorator('description')(
                            <Input placeholder={this.state.groupDetail.description} />)}
                    </Form.Item>
                    <Form.Item>
                    <Button style={{ width: '100%' }} type="primary" htmlType="submit">
                        Change Info
                    </Button>
                    </Form.Item>
                </Form>
                <Divider />

                <p><strong>Manage Members</strong></p>
                <br />
                <Select
                    mode="multiple"
                    style={{ width: '100%' }}
                    placeholder="Please select members to remove"
                    onChange={this.handleChange}
                >
                    {this.state.groupDetail.members.map((member) => (
                        <Option key={member.username}>
                            {member.screen_name}
                        </Option>
                    ))}
                </Select>
                <Button style={{ marginTop: '15px', width: '100%' }} type="danger" onClick={this.handleRemove}>
                    Remove
                </Button>
                <Divider />

                <p><strong>Manage Discipline</strong></p>
                <p>Check disciplines to remove them.</p>
                <p>Don't worry. It is easy to create them back.</p>
                {this.getOptions(this.state.groupDetail.rule)} 
                <br />
                <Button style={{ marginTop: '15px', width: '100%' }} type="primary" onClick={this.handleAddDiscipline}>
                    New Discipline
                </Button>
                <Divider />

                <p><strong>Manage Stories</strong></p>
                <br />
                <Select
                    mode="multiple"
                    style={{ width: '100%' }}
                    placeholder="Please select members to remove"
                    onChange={this.handleChange}
                >
                    {this.state.groupDetail.members.map((member) => (
                        <Option key={member.username}>
                            {member.screen_name}
                        </Option>
                    ))

                    }
                </Select>
                <Button style={{ marginTop: '15px', width: '100%' }} type="danger" onClick={this.handleRemove}>
                    Remove
                </Button>
                {
                    this.state.newItem ? 
                        <div className='popForm'>
                            <div className='popInner'>
                                {/* judge item type */}
                                {/* <WrappedGroupForm callback={this.fetch} that={this} /> */}
                                <Icon onClick={this.toggle} style={{ color: 'rgba(0, 0, 0, 0.7)', float: 'right' }}  type="close-circle" />
                            </div>
                        </div> : null
                }
            </div>
        )
    }
}

const GroupManage = Form.create()(NakedManage);

const mapStateToProps = (state) => {
    return {
        token: state.writers.token,
        screen_name: state.writers.screen_name
    }
}

export default connect(mapStateToProps)(GroupManage);

