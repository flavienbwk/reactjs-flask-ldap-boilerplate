import React from 'react';
import { Nav, Navbar } from 'react-bootstrap';
import styled from 'styled-components';
import { Link } from 'react-router-dom';
import packageJson from '../package.json';

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

export const NavigationBar = () => (
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
                    <Nav.Link as={Link} to={'/'}>Search</Nav.Link>
                    <Nav.Link as={Link} to={'/about'}>About</Nav.Link>
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    </Styles>
)