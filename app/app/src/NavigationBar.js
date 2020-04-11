import React, { Component } from 'react'
import { Nav, Navbar, Button } from 'react-bootstrap'
import { Auth } from './utils/Auth'
import styled from 'styled-components'
import { Link } from 'react-router-dom'
import packageJson from '../package.json'

const Styles = styled.div`
    .navbar {
        background-color: #222;
    }

    .navbar-brand, .navbar-nav .nav-link {
        color: #bbb;

        &:hover {
            color: white;
        }
    }

    .brand-image {
        max-width: 64px;
        height: 30px;
        padding-right: 16px;
    }
`;

export class NavigationBar extends Component {

    constructor(props) {
        super(props)
        this.auth = new Auth([ this.props.onAuthUpdate ])
    }

    render() {
        return (
            <Styles>
                <Navbar bg="light" expand="lg">
                    <Navbar.Brand as={Link} to={'/'}>
                        <img
                            alt="Logo My Project"
                            src={packageJson["homepage"] + "/logo.png"}
                            className="d-inline-block align-top brand-image"
                        />
                        {'My Project'}
                    </Navbar.Brand>
                    <Navbar.Toggle aria-controls="basic-navbar-nav" />
                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className="ml-auto">
                            {
                                (this.props.authenticated)
                                ? 
                                <>
                                    <Nav.Link as={Link} to={'/dashboard'}>Dashboard</Nav.Link>
                                    <Button variant="default" onClick={this.auth.logoutUser}>Logout</Button>
                                </>
                                : 
                                <Nav.Link as={Link} to={'/login'}>Login</Nav.Link>
                            }
                            <Nav.Link as={Link} to={'/about'}>About</Nav.Link>
                        </Nav>
                    </Navbar.Collapse>
                </Navbar>
            </Styles>
        )
    }

}

export default NavigationBar;