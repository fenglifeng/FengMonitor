var xmlHttp

//获得选中文件的文件名
function getCheckboxItem()
{
	var allSel="";
	if(document.form2.id.value) return document.form2.id.value;
	for(i=0;i<document.form2.id.length;i++)
	{
		if(document.form2.id[i].checked)
		{
			if(allSel=="")
				allSel=document.form2.id[i].value+ "`"+document.form2.room[i].value; 
			else
				allSel=allSel+"`"+document.form2.id[i].value+"`"+document.form2.room[i].value; ;
		}
	}
	return allSel;
}

//获得选中其中一个的id
function getOneItem()
{
	var allSel="";
	if(document.form2.id.value) return document.form2.id.value;
	for(i=0;i<document.form2.id.length;i++)
	{
		if(document.form2.id[i].checked)
		{
			allSel = document.form2.id[i].value;
			break;
		}
	}
	return allSel;
}
function selAll()
{
	for(i=0;i<document.form2.id.length;i++)
	{
		if(!document.form2.id[i].checked)
		{
			document.form2.id[i].checked=true;
		}
	}
}

function noSelAll()
{
	for(i=0;i<document.form2.id.length;i++)
	{
		if(document.form2.id[i].checked)
		{
			document.form2.id[i].checked=false;
		}
	}
}


function GetXmlHttpObject()
{
var xmlHttp=null;
try
 {
 // Firefox, Opera 8.0+, Safari
 xmlHttp=new XMLHttpRequest();
 }
catch (e)
 {
 // Internet Explorer
 try
  {
  xmlHttp=new ActiveXObject("Msxml2.XMLHTTP");
  }
 catch (e)
  {
  xmlHttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
 }
return xmlHttp;
}

function DelArc(aid)
{	

	var qstr=getCheckboxItem();
	xmlHttp=GetXmlHttpObject()

	if (xmlHttp==null){
	  	alert ("Browser does not support HTTP Request")
	  	return
	} 

	var url = "archives.php"
	url = url + "?&action=Delete&qstr="+qstr+""
	url = url + "&sid=" + Math.random()
	xmlHttp.onreadystatechange=stateChanged 
	xmlHttp.open("GET",url,true)
	xmlHttp.send(null)
} 

function stateChanged() 
{ 
if (xmlHttp.readyState==4 || xmlHttp.readyState=="complete")
 { 
 	if(xmlHttp.responseText.indexOf('ok!')>=0)
 	{
 		window.location.reload();
 	}
	document.getElementById("TestInfo").innerHTML=xmlHttp.responseText 
 } 
}