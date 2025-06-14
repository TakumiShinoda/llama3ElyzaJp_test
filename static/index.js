const API_HOST = 'http://localhost:5000'

const Socket = io()

function createSelectModelDropDownItemElements(modelList){
  let itemElements
  let itemElementsStr = ''

  if(
    (!Object.keys(modelList).indexOf('supportModels') < 0) ||
    (!Object.keys(modelList).indexOf('currentModel') < 0)
  ) return

  if(!Array.isArray(modelList['supportModels'])) return
  if(modelList['supportModels'].length <= 0) return

  for(let sm of modelList['supportModels']){
    itemElementsStr += /*html*/`
      <a class='list-group-item list-group-item-action list-group-item-success modelSelectDropdownMenuListItem'>${sm}</a>
    `
  }

  itemElements = $(itemElementsStr)

  return itemElements
}

async function reloadSelectModelDropDown(){
  let dropdownBtnElement = $('#modelSelectDropdownBtn')
  let dropdownMenuListElement = $('#modelSelectDropdownMenuList')
  let modelListApiResponse
  let modelListJson

  modelListApiResponse = await fetch(`${API_HOST}/getModelList`)
  modelListJson = JSON.parse(await modelListApiResponse.text())

  dropdownMenuListElement.empty()
  dropdownMenuListElement.append(createSelectModelDropDownItemElements(modelListJson))

  $('.modelSelectDropdownMenuListItem').on('click', async (ev) => {
    let selectedModel = $(ev.currentTarget).text()

    $('#modelSelectDropdownBtn').text(selectedModel)

    await fetch(`${API_HOST}/reloadModel?model=${selectedModel}`)
    await reloadSelectModelDropDown()
  })

  dropdownBtnElement.text(modelListJson['currentModel'])
}

$(async function (){
  await reloadSelectModelDropDown()
  $('body').css('display', 'flex')

  Socket.on('lockOperation', () => {
    console.log('lockOperation')
    $('#pageOverlayArea').css('display', 'flex')
  })

  Socket.on('unlockOperation', () => {
    console.log('unlockOperation')
    $('#pageOverlayArea').css('display', 'none')
  })

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