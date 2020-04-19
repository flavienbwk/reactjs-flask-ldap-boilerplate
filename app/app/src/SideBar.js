import React, { Component } from 'react'
import SideNav, { NavItem, NavIcon, NavText } from '@trendmicro/react-sidenav';
import ClickOutside from 'react-click-outsider'
import '@trendmicro/react-sidenav/dist/react-sidenav.css';
import { Route } from 'react-router-dom'
import { Auth } from './utils/Auth'
import { Person, QuestionCircle, BoxArrowInLeft, App } from 'react-bootstrap-icons'

export class SideBar extends Component {

    constructor(props) {
        super(props)
        this.auth = new Auth([ this.props.onAuthUpdate ])
        this.state = { "expanded": false }
    }

    render() {
        return (
            <Route render={({ location, history }) =>  (
                <React.Fragment>
                    <ClickOutside
                        onClickOutside={() => {
                            this.setState({ expanded: false });
                        }}
                    >
                        <SideNav
                            onSelect={(selected) => {
                                const to = '/' + selected;
                                if (location.pathname !== to) {
                                    history.push(to);
                                }
                            }}
                            expanded={this.state.expanded}
                            onToggle={(expanded) => {
                                this.setState({ expanded });
                            }}
                        >
                            <SideNav.Toggle />
                            <SideNav.Nav defaultSelected={
                                (location.pathname === "/login") 
                                ? "dashboard"
                                : location.pathname.substring(1)
                            }>
                                <NavItem eventKey="dashboard">
                                    <NavIcon>
                                        <App size={24}/>
                                    </NavIcon>
                                    <NavText>
                                        Dashboard
                                    </NavText>
                                </NavItem>
                                <NavItem eventKey="about">
                                    <NavIcon>
                                        <QuestionCircle size={24}/>
                                    </NavIcon>
                                    <NavText>
                                        About
                                    </NavText>
                                </NavItem>
                                {
                                    (this.props.authenticated)
                                    ?
                                        <NavItem eventKey="profile">
                                        <NavIcon>
                                            <Person size={24}/>
                                        </NavIcon>
                                        <NavText>
                                            Profile
                                        </NavText>
                                        </NavItem>
                                    :
                                        <></>
                                }
                                <NavItem eventKey="login" onClick={() => { if (this.props.authenticated) { return this.auth.logoutUser() } }}>
                                    <NavIcon>
                                        <BoxArrowInLeft size={24}/>
                                    </NavIcon>
                                    <NavText>
                                        {
                                            (this.props.authenticated)
                                            ? "Logout"
                                            : "Login"
                                        }
                                    </NavText>
                                </NavItem>
                            </SideNav.Nav>
                        </SideNav>
                    </ClickOutside>
                </React.Fragment>
                )}
            />
        )
    }

}

export default SideBar;