import React, {useEffect, useState} from "react"
import {Button, Card, Form, Col, DropdownButton, Dropdown, Row} from "react-bootstrap";
import axios from "axios";
import {API_SERVER} from "../../config/constant";
import {useSelector} from "../../store";


const CustomToggle = React.forwardRef(({children, onClick}, ref) => (
    <a
        href=""
        ref={ref}
        onClick={(e) => {
            e.preventDefault();
            onClick(e);
        }}
    >
        {children}
        <i className="feather icon-menu pointer-event"/>
    </a>
));


const QuestionCard = ({data, onDelete}) => {
    const [revealed, setRevealed] = useState(false)
    const account = useSelector((state) => state.account)

    const remove = () => {
        axios.delete(API_SERVER + `sections/${1}/questions/${data.id}`, {
            headers: {Authorization: `Bearer ${account.token}`}
        })
            .then(response => {
                onDelete(data.id);
            })
            .catch(error => {
            })
    }

    return (
        <Row>
            <Col lg={12}>
                <Card className="m-3">
                    <Card.Body>
                        <Card.Title className="d-flex justify-content-between">
                            <div className="pr-2">
                                <span>{data.content}</span>
                                <span className={revealed ? `d-inline` : `d-none`}> {data.gpt_answer}</span>
                            </div>
                            <Dropdown alignRight={true}>
                                <Dropdown.Toggle as={CustomToggle}>
                                </Dropdown.Toggle>

                                <Dropdown.Menu>
                                    <Dropdown.Item
                                        href="#"
                                        onClick={() => setRevealed(true)}
                                    >
                                        Reveal
                                    </Dropdown.Item>
                                    <Dropdown.Item href="#" onClick={remove}>Delete</Dropdown.Item>
                                </Dropdown.Menu>
                            </Dropdown>
                        </Card.Title>
                        <Form>
                            <Form.Group>
                                <Form.Control as="textarea" rows={3}/>
                            </Form.Group>
                        </Form>
                    </Card.Body>
                </Card>
            </Col>
        </Row>
    )
}

export default QuestionCard