import 'react-notifications/lib/notifications.css';
import React, { Component } from 'react'
import { Container, Row, Col, Card, Jumbotron, Form, Button } from 'react-bootstrap'
import { NotificationContainer } from 'react-notifications'
import { Auth } from './utils/Auth'
import { Ping } from './utils/Ping'
import { Notifier } from './utils/Notifier'
import styled from 'styled-components'

const Styles = styled.div`
    .paddind-top {
        padding-top: 16px;
    }

    .center {
        width: fit-content;
        text-align: center;
        margin: 1em auto;
        display: table;
    }

    .main-search-bar {
        padding: 32px;
        margin-top: 32px;
        margin-bottom: 8px;
    }
`

export class Login extends Component {

    constructor(props) {
        super(props);
        this.auth = new Auth(this.onAuthUpdate)
        this.state = {
            "username": "",
            "password": "",
            "disable_form": false,
            "login_btn_text": "Login",
            "authenticated": this.auth.isUserAuthenticated(),
            "profile": this.auth.getUserProfileCookie()
        }
    }

    onAuthUpdate = () => {
        this.setState({
            "authenticated": this.auth.isUserAuthenticated(),
            "profile": this.auth.getUserProfileCookie()
        })
    }

    onUsernameChange = (event) => this.setState({ "username": event.target.value })
    
    onPasswordChange = (event) => this.setState({ "password": event.target.value })

    onFormSubmitted = async (event) => {
        if (this.state.username.length && this.state.password.length) {
            this.setState({ 
                "disable_form": true,
                "login_btn_text": "Connecting..."
            })
            let disable_form = false
            const api_ping_query = await Ping.pingApi()
            if (api_ping_query) {
                const api_auth_query = await this.auth.requestLDAPLogin(this.state.username, this.state.password)
                if (api_auth_query && api_auth_query.error === false) {
                    this.auth.registerUserAuthentication(
                        this.state.username,
                        api_auth_query
                    )
                    // @todo TODO(flavienbwk): Redirect the user to dashboard
                    disable_form = true
                } else {
                    Notifier.notifyFromResponse(api_auth_query, "Authentication")
                }
            } else {
                Notifier.createNotification(
                    "error", 
                    "API unreachable", 
                    "Please check your internet connection"
                )
            }
            this.setState({ 
                "disable_form": disable_form,
                "login_btn_text": "Login"
            })
        }
    }

    render() {
        return (
            <Styles>
                <Container>
                    <Row className="paddind-top">
                        <NotificationContainer />
                        <Col lg={{ offset: 3, span: 6 }}>
                            <Card>
                                <Card.Body>
                                    <Jumbotron>
                                        <h1>Login</h1>
                                        <p>
                                            Login to the application with your LDAP credentials to access your dashboard.
                                        </p>
                                    </Jumbotron>
                                    {
                                        (this.state.authenticated === false)
                                        ?
                                        (
                                            <Form>
                                                <Form.Group>
                                                    <Form.Label>Username</Form.Label>
                                                    <Form.Control 
                                                        type="text" 
                                                        placeholder="LDAP username"
                                                        disabled={this.state.disable_form}
                                                        onChange={this.onUsernameChange}
                                                    />
                                                </Form.Group>
                                                <Form.Group>
                                                    <Form.Label>Password</Form.Label>
                                                    <Form.Control 
                                                        type="password" 
                                                        placeholder="LDAP password"
                                                        disabled={this.state.disable_form}
                                                        onChange={this.onPasswordChange}
                                                    />
                                                </Form.Group>
                                                <Button 
                                                    variant="primary" 
                                                    type="submit" 
                                                    style={{ width: "100%" }} 
                                                    disabled={this.state.disable_form}
                                                    onClick={this.onFormSubmitted}
                                                >
                                                    { this.state.login_btn_text }
                                                </Button>
                                            </Form>
                                        )
                                        :
                                        <div>
                                            <h3 className="center">You are already authenticated !</h3>
                                            <p className="center">
                                                { 
                                                    this.state.profile !== undefined && "first_name" in this.state.profile 
                                                    ? this.state.profile.first_name 
                                                    : "Tell me" 
                                                }, do you want to :
                                            </p>
                                            <ul>
                                                <li>Go to your dashboard ?</li>
                                                <li><button onClick={this.auth.logoutUser}>Logout ?</button></li>
                                            </ul>
                                        </div>    
                                    }
                                </Card.Body>
                            </Card>
                        </Col>
                    </Row>
                </Container>
            </Styles>
        )
    }

    componentDidMount() {
        document.title = "Login - My Project";
    }

}
