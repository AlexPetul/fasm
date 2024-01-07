import React from "react"

import { Input } from 'antd';
import "./Input.css"


export const FormInput = ({type, placeholder, value, onChange, style}) => {
    return (
        <>
            <Input
                type={type}
                className="input-control"
                placeholder={placeholder}
                size="large"
                value={value}
                onChange={onChange}
                style={style}
            />
        </>
    )
}