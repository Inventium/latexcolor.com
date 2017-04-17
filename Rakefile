# frozen_string_literal: true

namespace :color do
  _targetdir = 'site'

  desc 'Delete generated _site files'
  task :clean do
    system 'rm -fR _site *~'
  end

  desc 'Run the jekyll dev server'
  task :server do
    system 'jekyll --server --auto'
  end

  desc 'Build the pages.'
  task :compile do
    system './colorproc.rb > _partials/colors.html.erb'
    system './erb_run.rb index.html.erb > index.html'
    system './erb_run.rb oh-no.html.erb > oh-no.html'
    system './erb_run.rb thank-you.html.erb > thank-you.html'
    system './erb_run.rb about.html.erb > about.html'
  end
end

namespace :compass do
  desc 'Delete temporary compass files'
  task :clean do
    system 'rm -fR css/*'
  end

  desc 'Run the compass watch script'
  task :watch do
    system 'compass watch'
  end

  desc 'Compile sass scripts'
  task compile: [:clean] do
    system 'compass compile'
  end
end
