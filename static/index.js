const API_HOST = 'http://localhost:5000'

$(function (){
  $('#talkFormBtn').on('click', async () => {
    let formInputElement = $('#talkFormInput')
    let chatAreaElement = $('#chatArea')
    let apiResponse
    let responseText
    
    if(
      (formInputElement.val() == undefined) || 
      (formInputElement.val() == '')
    ) return

    apiResponse = await fetch(`${API_HOST}/talk?inputText=${formInputElement.val()}`)
    responseText = await apiResponse.text()

    console.log(responseText)
    chatAreaElement.text(responseText)
  })
})