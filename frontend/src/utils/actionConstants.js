export const ACTION_LABELS = {
  click: '点击',
  click_image: '图像点击',
  input: '输入',
  wait_until_exists: '等待元素',
  assert_text: '文本断言',
  assert_image: '图像断言',
  swipe: '滑动',
  sleep: '强制等待',
  extract_by_ocr: 'OCR提取变量',
  start_app: '启动应用',
  stop_app: '停止应用',
  back: '返回',
  home: '主页',
}

export const ACTION_COLORS = {
  click: '#667eea',
  click_image: '#764ba2',
  input: '#f093fb',
  wait_until_exists: '#4facfe',
  assert_text: '#fa709a',
  assert_image: '#ff8a65',
  swipe: '#30cfd0',
  sleep: '#e6a23c',
  extract_by_ocr: '#67c23a',
  start_app: '#43a047',
  stop_app: '#e53935',
  back: '#78909c',
  home: '#5c6bc0',
}

export function getActionLabel(action) {
  return ACTION_LABELS[action] || action
}

export function getActionColor(action) {
  return ACTION_COLORS[action] || '#909399'
}
