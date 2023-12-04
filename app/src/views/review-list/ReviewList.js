import React, {useEffect, useState} from "react"
import {Col, Row} from "react-bootstrap";
import axios from "axios";
import {API_SERVER} from "../../config/constant";
import {useSelector} from "../../store";
import Spinner from "../../components/Spinner/Spinner";
import QuestionReviewCard from "../../components/QuestionCard/QuestionReviewCard";


const ReviewList = () => {
    const account = useSelector((state) => state.account);
    const [questions, setQuestions] = useState([])
    const [isLoading, setIsLoading] = useState(true)
    const [selected, setSelected] = useState([])

    const fetchQuestions = () => {
        axios.get(API_SERVER + `sections/questions`, {headers: {Authorization: `Bearer ${account.token}`}})
            .then(response => {
                setQuestions(response.data)
                setIsLoading(false);
            })
            .catch(error => {
                setIsLoading(false);
            })
    }

    useEffect(() => {
        fetchQuestions()
    }, [])

    const onSelect = (id) => {
        setSelected([id, ...selected]);
    }

    const onDeSelect = (id) => {
        setSelected(selected.filter((x) => x !== id))
    }

    return (
        <div>
            {isLoading ? <Spinner/> : null}
            <Row>
                <Col lg={12}>
                    <div className="d-inline-block"><h3>Review</h3></div>
                </Col>
            </Row>
            {questions.map((data) =>
                <QuestionReviewCard
                    data={data}
                    onDelete={null}
                    onSelect={null}
                    onDeSelect={null}
                />
            )}
        </div>
    )
}

export default ReviewList;