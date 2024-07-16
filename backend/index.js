import express from 'express'
import cors from 'cors'
import {spawn} from 'child_process'

const app = express()
// app.use(cors)
// app.use(express.json())


app.get('/', (req, res)=>{
    console.log('connected')
    res.send('connected')
})

app.get('/maintenance_cost/:dict', async(req, res)=>{
    const dict = req.params.dict
    JSON.parse(dict)
    const pyProc =await  spawn('python', ['scripts/regressor.py','cost', dict ])
    var result, err, flag = 1;

    pyProc.stderr.on('data', (data)=>{
        flag = 0;
        err = data.toString()
    })
    pyProc.stdout.on('data', (data)=>{
        result = data.toString()
    })

    pyProc.on('exit', (code)=>{
        if (flag === 0) res.status(404).send(err)
        else res.status(200).send(result)
    })
})
app.get('/maintenance_date/:dict', async(req, res)=>{
    const dict = req.params.dict
    JSON.parse(dict)
    const pyProc =await  spawn('python', ['scripts/regressor.py','date', dict ])
    var result, err, flag = 1;

    pyProc.stderr.on('data', (data)=>{
        flag = 0;
        err = data.toString()
    })
    pyProc.stdout.on('data', (data)=>{
        result = data.toString()
    })

    pyProc.on('exit', (code)=>{
        if (flag === 0) res.status(404).send(err)
        else res.status(200).send(result)
    })
})

app.listen(8888, ()=>{
    console.log('listening at port 8888')
})