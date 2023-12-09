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


const QuestionCard = ({data, sectionId, onDelete, onSelect, onDeSelect}) => {
    const [revealed, setRevealed] = useState(false)
    const [answer, setAnswer] = useState(data.user_answer)
    const [selected, setSelected] = useState(false)
    const account = useSelector((state) => state.account)

    const remove = () => {
        axios.delete(API_SERVER + `sections/${sectionId}/questions/${data.id}`, {
            headers: {Authorization: `Bearer ${account.token}`}
        })
            .then(response => {
                onDelete(data.id);
            })
            .catch(error => {
            })
    }

    const save = () => {
        axios.patch(API_SERVER + `sections/${sectionId}/questions/${data.id}`, {user_answer: answer}, {
            headers: {Authorization: `Bearer ${account.token}`}
        })
            .then(response => {

            })
            .catch(error => {
            })
    }

    const onChangeSelect = (e) => {
        if (e.target.checked) {
            onSelect(data.id)
        } else {
            onDeSelect(data.id)
        }
        setSelected(!selected);
    }

    return (
        <Row>
            <Col lg={12}>
                <Card className={`m-3 pt-3 ${data.for_review ? 'for-review' : ''}`}>
                    {data.for_review === false ?
                        <Form.Check
                            type="checkbox"
                            className="position-absolute"
                            checked={selected}
                            onChange={onChangeSelect}
                            style={{top: 10, left: 10}}
                        /> : null}
                    <Card.Body className="pt-50">
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
                                <Form.Control
                                    as="textarea"
                                    rows={3}
                                    onBlur={() => save()}
                                    onChange={(e) => setAnswer(e.target.value)}
                                    value={answer}
                                />
                            </Form.Group>
                            {data.reviewer_answer ?
                                <Form.Group>
                                    <Form.Control
                                        as="textarea"
                                        rows={3}
                                        value={data.reviewer_answer}
                                        readOnly={true}
                                    />
                                </Form.Group> : null}
                        </Form>
                    </Card.Body>
                </Card>
            </Col>
        </Row>
    )
}

export default QuestionCard