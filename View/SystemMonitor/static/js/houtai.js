// 新增   
function trdadd(){   
  flag=false;   
  document.getElementById("fid").style.display="block"; //控制显示   
  chongzhi();   
  document.getElementById("aid").disabled=false; //重新启用     
}   
  
//保存   
function baocun(){   
      if(flag==false){         
          add(flag);   
          document.getElementById("fid").style.display="none";   
      }else{   
    
     
        add(flag);   
        document.getElementById("fid").style.display="none";   
         
      }   
}   
  
//重置   
function chongzhi(){   
 document.getElementById("myform").reset();   
}   
  
//删除        
function deleteRow(input){   
    var s=input.parentNode.parentNode.rowIndex;   
    document.getElementById("tableid").deleteRow(s);   
    var num=document.getElementById("tableid").rows.length;   
    for(var i=1;i<num;i+=1){   
       table.rows[i].cells[0].innerHTML=i; //把每行的每一列设为i   
         
       }   
       alert("删除成功！！");   
}   
var table=document.getElementById("tableid");   var flag=false;   
var getselectrow;   
function getNum(){   
     var haoRow=table.rows[0];   
     return haoRow.cells.length;   
}   
  
//添加方法   
  
function add(flag){   
    
  // var num=getNum();   
   var row=table.insertRow(-1); //为-1时往下加（升序），为0时往上加（id降序）   
   var add1=row.insertCell(0);   
   var add2=row.insertCell(1);   
   var add3=row.insertCell(2);   
   var add4=row.insertCell(3);   
   var add5=row.insertCell(4);   
   var add6=row.insertCell(5); 
   var add7=row.insertCell(6);
   var add8=row.insertCell(7);
   var add9=row.insertCell(8);  
   add1.innerHTML=document.getElementById("tableid").rows.length-1;//不加-1时id从二开始；原因：标题占一个
   add2.innerHTML=document.getElementById("").value; 
   add3.innerHTML=document.getElementById("title").value; 
   var tall=document.getElementById("catid");   
   var   index=tall.selectedIndex;// 当前坐标   
   var option=tall.options[index];  
   add4.innerHTML=option.text;  
   add5.innerHTML=document.getElementById("homeid").options[document.getElementById("homeid").selectedIndex].text;   
   add6.innerHTML=document.getElementById("atid").options[document.getElementById("atid").selectedIndex].text;   
   add7.innerHTML=document.getElementById("atid").options[document.getElementById("atid").selectedIndex].text;  
 
  add8.innerHTML="<input type='button' value='修改' onclick='updateRow(this)'> <input type='button' value='删除' onclick='deleteRow(this)'>";   
  add8.innerHTML="<a href='' onclick='deleteRow(this)' value='删除'>";  
  alert("添加成功！！");   
   
  // }
  // else{    
  //    var row2=table.rows[getselectrow];//选中当前行   
  //           //把修改后的值设置到对应的文本框中   
  //    row2.cells[1].innerHTML=document.getElementById("aid").value;   
  //    row2.cells[2].innerHTML=document.getElementById("bid").value;   
  //    row2.cells[3].innerHTML=document.getElementById("cid").value;   
  //    var pall=document.getElementById("eid");   
  //    var index=pall.selectedIndex; //当前坐标   
  //    var option=pall.options[index];   
  //    row2.cells[4].innerHTML=option.text;   
       
  //    alert("修改成功！！");   
  // }       
  }   
       
      //修改   
     function updateRow(input){   
     flag=true  
     document.getElementById("aid").disabled=true;   //不能启用   
     document.getElementById("fid").style.display="block";   
       
     var i=input.parentNode.parentNode.rowIndex;   
     
        getselectrow=i;   
           //得到选中行的内容放到文本框   
     document.getElementById("aid").value=table.rows[i].cells[1].innerHTML;   
     document.getElementById("bid").value=table.rows[i].cells[2].innerHTML;   
     document.getElementById("cid").value=table.rows[i].cells[3].innerHTML;   
  
      var select=document.getElementById("eid");   
        var index=select.selectedIndex;// 当前坐标   
        var option= select.options[index];   
        option.text=table.rows[i].cells[4].innerHTML;   
       
    }            
  