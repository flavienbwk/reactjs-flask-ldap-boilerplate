import React, { Component } from 'react'
import { Container, Row, Col, Jumbotron, } from 'react-bootstrap';
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
`

class Dashboard extends Component {

    render() {
        return (
            <Styles>
                <Container>
                    <Row className="paddind-bottom">
                        <Col lg={{ span: 12 }} className="center">
                            <Jumbotron>
                                <h1>Hello</h1>
                                <p>
                                    You are on your dashboard page.
                                </p>
                            </Jumbotron>
                        </Col>
                    </Row>
                </Container>
            </Styles>
        )
    }

    componentDidMount() {
        document.title = "Dashboard - My Project";
    }

}

export default Dashboard;