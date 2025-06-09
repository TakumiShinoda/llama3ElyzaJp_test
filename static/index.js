const API_HOST = 'http://localhost:5000'

$(function (){
  $('#talkFormBtn').on('click', async () => {
    let formInputElement = $('#talkFormInput')
    let chatAreaElement = $('#chatArea')
    let loadingAnimElement = $('#chatLoadingAnim')
    let apiResponse
    let responseText
    
    if(
      (formInputElement.val() == undefined) || 
      (formInputElement.val() == '')
    ) return

    chatAreaElement.text('')
    loadingAnimElement.css('display', 'flex')
    apiResponse = await fetch(`${API_HOST}/talk?inputText=${formInputElement.val()}`)
    responseText = await apiResponse.text()
    loadingAnimElement.css('display', 'none')
    chatAreaElement.text(responseText)
  })
})