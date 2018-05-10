Rails.application.routes.draw do
  get 'history/history'
  get 'dictionary/dictionary'
  get 'homepage/index'
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
  resources :articles
  root 'homepage#index'
end
