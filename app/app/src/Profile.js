import React, { Component } from 'react'
import { Container, Nav, Row, Col, Jumbotron, Table, Form, Button } from 'react-bootstrap'
import Loader from 'react-loader-spinner'
import { Redirect } from 'react-router-dom'
import { Link } from 'react-router-dom'
import { Auth } from './utils/Auth'
import styled from 'styled-components'

const Styles = styled.div`
    .paddind-bottom {
        padding-bottom: 16px;
    }

    .center {
        width: fit-content;
        text-align: center;
        margin: 1em auto;
        display: table;
    }

    .left {
        width: fit-content;
        text-align: left;
        margin: 0;
        display: block;
    }
`

export class Profile extends Component {

    constructor(props) {
        super(props);
        this.auth = new Auth()
        this.state = {
            "disable_form": false,
            "profile": this.auth.getUserProfile() 
        }
    }

    render() {
        if (this.props.authenticated === false)
            return <Redirect to='/login' />
        return (
            <Styles>
                <Container>
                    <Row className="paddind-bottom">
                        <Col lg={{ span: 12 }} className="center">
                            <Jumbotron>
                                <h1>Edit your profile</h1>
                            </Jumbotron>
                            <Nav.Link as={Link} to={'/dashboard'} className="left">
                                <Button variant="secondary">&lt; Dashboard</Button>
                            </Nav.Link>
                            <Form>
                                <Table striped bordered hover>
                                    <thead>
                                        <tr>
                                            <th>Name</th>
                                            <th>Value</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>Email address</td>
                                            <td>
                                                <Form.Control 
                                                    type="email"
                                                    placeholder="Enter email"
                                                    defaultValue={ this.state.profile.email }
                                                    disabled={ this.state.disable_form }
                                                />
                                            </td>
                                        </tr>
                                        <tr>
                                            <td colSpan={2}>
                                                <Button 
                                                    variant="primary" 
                                                    type="submit"
                                                    disabled={ this.state.disable_form }
                                                >
                                                    {
                                                        this.state.disable_form
                                                        ?
                                                        <Loader
                                                            type="TailSpin"
                                                            color="#fff"
                                                            height={28}
                                                            width={28}
                                                        />
                                                        :
                                                        <>Validate</>
                                                    }
                                                </Button>
                                            </td>
                                        </tr>
                                    </tbody>
                                </Table>
                            </Form>
                        </Col>
                    </Row>
                </Container>
            </Styles>
        )
    }

    componentDidMount() {
        document.title = "Profile - My Project";
    }

}

export default Profile;