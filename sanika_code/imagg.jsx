import React from 'react';
import { useState } from 'react';
import Background from '../containers/1.png';
import $ from "jquery";
import img from '../containers/car.png';
var sectionStyle = {
    width: "100%",
    height: "900px",
    backgroundImage: `url(${Background})`, // main background file
    paddingLeft: "0px"
};
var carStyle={}
var arr=[0,0,0,0,0,0,0,0,0,0];
var movingAvg = [];
var smoothingWindow = 10;
var i=0;
var j=0;
var mean=0;
var m=0;
var k;
function Imgg() {

    // console.log("main");
    updateData();
    const [pos,setPos]=useState(0);

   //setInterval(updateData, 10000);
    // const [items,setItems]=useState([]);

    // const addItem = (d) =>{
    //     setItems([ ...items,{
    //         id:items.lenght,
    //         value:d
    //     }])

    //     console.log("array element"+d);
    // }
    function writearray(d)
    {
       

        d=d.split('\n',10);
        console.log(d);
        d = Number(d[0]);
        console.log('data', d, 'type of data ', typeof d, 'smoothingWindow', smoothingWindow);
        // append to array
        movingAvg.push(d)
        console.log(movingAvg);

        if (movingAvg.length >= smoothingWindow) {
            // removes first value if length reaches smoothing window (eg 10)
            movingAvg.shift();
        }
        // get sum
        var tempAvg = 0;
        console.log('tempAvg: ' + tempAvg + ' movingAvg ', movingAvg);
        movingAvg.forEach(element => {
            tempAvg += element;
        });
        // get average
        tempAvg /= movingAvg.length;
        setPos(tempAvg);
        // console.log('tempAvg: ' + tempAvg);
        console.log('tempAvg: ' + tempAvg+'--pos: '+pos);

        //return tempAvg;
        
       
    } 

    function updateData() {
        $(document).ready(function(){
            // console.log("ma");
			jqueryAjax();
			setInterval(jqueryAjax, 1000); // to resend requests
        });
        
       
        
		function jqueryAjax () {
			var ajaxtext = "";
			$.ajax('http://localhost/ids/getData.php',{
				success: function(data) {
                    // console.log(data);
                    // console.log(typeof(data));    
                    writearray(data);
                    // setPos(writearray(data));
                    // console.log("pos="+pos);
					
					}
                 });	             
			}      
    }

    return (
        <div id="sdf">
            <div style={sectionStyle}>
                <div >
                    {/* <img src={img} alt="Image" width="600" style={{ top: "500px", left:pos + "px", position: "relative" }} /> */}
                </div>
                <h1>{"Position="+pos}</h1>
            </div>
            
        </div>


    );
}
export default Imgg;